from django.contrib.auth.models import User
from .models import Post
from rest_framework.test import APITestCase
from rest_framework import status


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='Post 1')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'A good title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'A good title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brad = User.objects.create_user(username='brad', password='pass')
        Post.objects.create(owner=adam, title='A title')
        Post.objects.create(owner=brad, title='Another title')

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'A title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'A new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, 'A new title')
   
    def test_user_cannot_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'A new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)