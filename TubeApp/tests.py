from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Video

class VideoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_video(self):
        response = self.client.post('/api/videos/', {'name': 'Test Video', 'video_url': 'http://test.com/video.mp4'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.get().name, 'Test Video')

    def test_get_videos(self):
        Video.objects.create(user=self.user, name='Test Video', video_url='http://test.com/video.mp4')
        response = self.client.get('/api/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_video(self):
        video = Video.objects.create(user=self.user, name='Test Video', video_url='http://test.com/video.mp4')
        response = self.client.put(f'/api/videos/{video.id}/', {'name': 'Updated Video', 'video_url': 'http://test.com/updated_video.mp4'})
        self.assertEqual(response.status_code, 200)
        video.refresh_from_db()
        self.assertEqual(video.name, 'Updated Video')

    def test_delete_video(self):
        video = Video.objects.create(user=self.user, name='Test Video', video_url='http://test.com/video.mp4')
        response = self.client.delete(f'/api/videos/{video.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Video.objects.count(), 0)
