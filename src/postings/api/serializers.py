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