from rest_framework import generics

from postings.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostAPIView(generics.CreateAPIView):
	lookup_field 		= 'pk'
	serializer_class 	= BlogPostSerializer

	def get_queryset(self):
		return BlogPost.objects.all()

	def perform_create(self, serializer):	# user가 read_only라서 api창에서 꼭 골라야한다는 에러가 뜨는데, 이 코드로 request.user 받게끔 설정해 줌
		serializer.save(user=self.request.user)


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field 		= 'pk'
	serializer_class 	= BlogPostSerializer

	def get_queryset(self):
		return BlogPost.objects.all()

