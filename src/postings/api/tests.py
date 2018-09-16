from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler 	= api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth import get_user_model
from postings.models import BlogPost

from rest_framework.reverse import reverse as api_reverse


User = get_user_model()

class BlogPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User(username='testCobee', email='test@test.com')
		user_obj.set_password("randompw")
		user_obj.save()
		blog_post = BlogPost.objects.create(
										user=user_obj,
										title='New Title',
										content='New Content'
										)

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_post(self):
		post_count = BlogPost.objects.count()
		self.assertEqual(post_count, 1)

	def test_get_list(self):
		data = {}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_post_item(self):
		data = {"title": "random changed", "content": "is it real?"}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_get_item(self):
		blog_post = BlogPost.objects.first()
		data = {}
		url = blog_post.get_api_url()
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_item(self):
		blog_post = BlogPost.objects.first()
		url = blog_post.get_api_url()
		data = {"title": "random changed", "content": "is it real?"}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


	def test_update_item_with_user(self):
		blog_post = BlogPost.objects.first()
		url = blog_post.get_api_url()
		data = {"title": "random changed", "content": "is it real?"}
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) 	# JWT token header
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_post_item_with_user(self):
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
		data = {"title": "random changed", "content": "is it real?"}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_ownership(self):
		owner = User.objects.create(username='testuser2')
		blog_post = BlogPost.objects.create(
										user=owner,
										title='New Title',
										content='New Content'
										)

		user_obj = User.objects.first()
		self.assertNotEqual(user_obj.username, owner.username)
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

		url = blog_post.get_api_url()
		data = {"title": "random changed", "content": "is it real?"}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


