from rest_framework import serializers

from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):		# JSON형식으로 convert 후 data validation
	url 	= serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BlogPost
		fields = [
			'url',
			'id',
			'user',
			'title',
			'content',
			'timestamp',
		]
		read_only_fields = ['id', 'user']		# 수정 불가능하게 만듬

	def get_url(self, obj):
		request = self.context.get("request")
		return obj.get_api_url(request=request)