from django.db.models import Q
from rest_framework import generics, mixins

from postings.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer


class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field 		= 'pk'
	serializer_class 	= BlogPostSerializer

	def get_queryset(self):
		qs = BlogPost.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(
					Q(title__icontains=query)|		# Q의 사용은 'or, 즉|' 을 가능하게 해줌
					Q(content__icontains=query)
					).distinct()
		return qs

	def perform_create(self, serializer):	# user가 read_only라서 api창에서 꼭 골라야한다는 에러가 뜨는데, 이 코드로 request.user 받게끔 설정해 줌
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request": self.request}


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field 		= 'pk'
	serializer_class 	= BlogPostSerializer
	permission_classes	= [IsOwnerOrReadOnly]		# owner, 즉 user를 제외한 접근은 read only. it's all about permissions

	def get_queryset(self):
		return BlogPost.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		return {"request": self.request}
