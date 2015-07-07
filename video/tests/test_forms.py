from django.test import TestCase

from ..forms import (
    VIDEO_NAME_FIELD_REQUIRED_ERROR,
    VIDEO_URL_FIELD_REQUIRED_ERROR,
    VideoForm
)
from ..utils import get_youtube_id_from_url, VIDEO_URL_FIELD_INVALID_ERROR 

class VideoFormTest(TestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'videos.json',
    ]
    
    def test_form_include_correct_fields(self):
        form = VideoForm()
        expected_fields = ['name', 'url']
        [self.assertIn(field, form.fields) for field in expected_fields]

    def test_form_has_correct_field_ids(self):
        """ Correct id attributes for widgets are rendered """

        form = VideoForm()
        self.assertEqual(
            form.fields['name'].widget.attrs['id'], 'id_video_title')

    def test_form_renders_correct_fields(self):
        form = VideoForm()
        self.assertIn('id_video_title', form.as_p())
        self.assertIn('id_video_url', form.as_p())

    def test_form_has_correct_error_messages(self):
        # Missing required fields
        form = VideoForm(
            data={'course':u'1', 'name':'', 'url':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [VIDEO_NAME_FIELD_REQUIRED_ERROR],
            'url': [VIDEO_URL_FIELD_REQUIRED_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)

        # Invalid url
        form = VideoForm(
            data={'course':u'1', 'name':'Test', 'url':'htt://example.com'})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'url': [VIDEO_URL_FIELD_INVALID_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)
        
        # YouTube video id is wrong
        form = VideoForm(
            data={
                'course':u'1',
                'name':'Test',
                'url':'http://www.youtube.com/embed/ZJqxxtoolongYtyb9iERk'
            })
        self.assertFalse(form.is_valid())
        expected_errors = {
            'url': [VIDEO_URL_FIELD_INVALID_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)
