from rest_framework import serializers

from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):		# JSON형식으로 convert 후 data validation
	class Meta:
		model = BlogPost
		fields = [
			'pk',
			'user',
			'title',
			'content',
			'timestamp',
		]
		read_only_fields = ['user']		# 수정 불가능하게 만듬
		