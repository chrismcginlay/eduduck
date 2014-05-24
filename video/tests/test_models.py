from django.test import TestCase

from ..models import Video

class VideoTests(TestCase):
    """Test the models of the video app"""
    
    def test_can_create_a_video(self):
        yt_test_url = 'https://www.youtube.com/watch?v=xRVHylmxUk8'
        self.assertNotRaises(
            Video(name='Test', url=yt_test_url, lesson=None, course=1))
        self.assertNotRaises(
            Video(name='Test2', url=yt_test_url, lesson=1, course=None))
    
    def test_video_must_have_one_FK(self):
        self.assertRaises(Video(
            name='Test', url=yt_test_url, lesson=None, course=None))
    
    def test_video_url_must_resolve(self):
        self.fail("write me")