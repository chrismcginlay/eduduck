from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import TestCase

from core.eduduck_exceptions import CheckRepError
from courses.models import Course
from lesson.models import Lesson
from ..models import Video

import logging
logger = logging.getLogger(__name__)

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
    
    def setUp(self):
        self.yt_test_url = 'https://www.youtube.com/watch?v=xRVHylmxUk8'
        
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
        with self.assertRaises(CheckRepError): 
            Video.objects.create(
                name='Test', url=self.yt_test_url, 
                lesson=None, course=None)
            
    def test___unicode__(self):
        v = Video.objects.get(pk=1)
        self.assertEqual(v.__unicode__(), "Blender Course Intro")
        
    def test___str__(self):
        v = Video.objects.get(pk=1)
        self.assertEqual(v.__str__(), "Video: Blender Course Intro")

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
        v2.url = ""
        self.assertFalse(v1._checkrep())
        self.assertFalse(v2._checkrep())

    def test_save(self):
        v1 = Video.objects.get(pk=1)
        v2 = Video.objects.get(pk=2)
        v3 = Video.objects.get(pk=3)
        v1.save()
        with self.assertRaises(TypeError):
            v1.name=''
            v1.save()
        with self.assertRaises(TypeError):
            v2.url=''
            v2.save()
        with self.assertRaises(CheckRepError):
            v3.lesson = None
            v3.course = None
            v3.save()
            
    def test___init__(self):
        course = Course.objects.get(pk=1)
        lesson = Lesson.objects.get(pk=2)

        vOK1 = Video.objects.create(
            name = 'Test',
            url = 'https://www.youtube.com/watch?v=-Hl74zWStxs',
            course = course, lesson = None)
        vOK2 = Video.objects.create(
            name = 'Test',
            url = 'https://www.youtube.com/watch?v=-Hl74zWStxs', 
            course = None, lesson = lesson)
        v_http = Video.objects.create(
            name = 'Test',
            url = 'http://www.youtube.com/watch?v=-Hl74zWStxs',
            course = course, lesson = None)
        self.assertEqual(v_http.url[:8], 'https://')
        with self.assertRaises(CheckRepError) as cm:
            vDud1 = Video.objects.create(
                name = 'Test',
                url = 'https://www.youtube.com/watch?v=-Hl74zWStxs', 
                course = None, lesson = None)
        with self.assertRaises(TypeError) as cm:
            vDud2 = Video.objects.create(
                name = '',
                url = 'https://www.youtube.com/watch?v=-Hl74zWStxs', 
                course = course, lesson = None)
        with self.assertRaises(TypeError) as cm:
            vDud3 = Video.objects.create(
                name = 'Test', url = '', course = course, lesson = None)
        
    def test_emitted_url_always_uses_https_protocol(self):
        #Regardless of any user-provided protocol, video.url emits https:// 

        course = Course.objects.get(pk=1)
        v_http = Video.objects.create(
            name = 'Test',
            url = 'http://www.youtube.com/watch?v=-Hl74zWStxs',
            course = course, lesson = None)
        v_https = Video.objects.create(
            name = 'Test',
            url = 'https://www.youtube.com/watch?v=-Hl74zWStxs', 
            course = course, lesson = None)
        self.assertEqual(v_http.url[:8], 'https://')
        self.assertEqual(v_https.url[:8], 'https://')  
