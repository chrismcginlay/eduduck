from django.core.validators import URLValidator
from django.test import TestCase

from courses.models import Course, Lesson
from ..models import Video


class VideoTests(TestCase):
    """Test the models of the video app"""
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome_lints.json', 
        'videos.json',
        'attachments.json'
        ]
    
    #video1_data = {
        #'url': 'http://youtu.be/LIM--jfnKeU',
        #'name': 'Music introduction',
        #}
    
    #course1_data = {
        #'code': 'EDU02',
        #'name': 'A Course of Leeches',
        #'abstract': 'Learn practical benefits of leeches',
        #'level': 'Basic',
        #'credits': 30,
        #}
    
    #lesson1_data = {
        #'code': 'B1',
        #'name': 'Introduction to Music',
        #'abstract': 'A summary of what we cover',
        #}
    
    def setUp(self):
        pass
        self.yt_test_url = 'https://www.youtube.com/watch?v=xRVHylmxUk8'
        #self.video1 = Video(**self.video1_data)
        #self.course1 = Course(**self.course1_data)
        #self.course1.save()
        #self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        #self.lesson1.save()
        
    def test_can_create_a_video(self):
        Video(name='Test',
              url=self.yt_test_url,
              lesson=None,
              course=Course.objects.get(pk=1)
        )
        Video(name='Test2',
              url=self.yt_test_url, 
              lesson=Lesson.objects.get(pk=1),
              course=None
        )
    
    def test_video_must_have_one_FK(self):
        self.assertRaises(Video(name='Test', url=self.yt_test_url, lesson=None, course=None))

    def test___unicode__(self):
        v = Video.objects.get(pk=1)
        self.assertEqual(v.__unicode__(), "Blender Course Intro")
        
    def test___str__(self):
        v = Video.objects.get(pk=1)
        self.assertEqual(v.__str__(), "Video: Blender Course Intro")
        
    def test_video_link_url_must_resolve(self):
        v = Video.objects.get(pk=1)
        URLValidator(v.url)

    def test_get_absolute_url(self):
        #For now, this should just return the youtube link
        v = Video.objects.get(pk=1)
        URLValidator(v.get_absolute_url)
        self.assertTrue("youtube" in v.get_absolute_url())
        self.assertEqual(v.url, v.get_absolute_url())
        
    def test__checkrep(self):
        # Video should have a name and url
        v1 = Video.objects.get(pk=1)
        v2 = Video.objects.get(pk=2)
        self.assertTrue(v1._checkrep())
        self.assertTrue(v2._checkrep())
        v1.name = ""
        v1.save()
        v2.url = ""
        v2.save()
        self.assertFalse(v1._checkrep())
        self.assertFalse(v2._checkrep())
