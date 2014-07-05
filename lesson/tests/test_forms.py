from django.test import TestCase

from ..forms import LessonEditForm 
from ..models import Lesson

class LessonFormTests(TestCase):
    """ Test the forms of the lesson app """
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
    ]
    
    def test_form_has_correct_field_ids(self):
	""" Correct id attributes for widgets are rendered """
	
	form = LessonEditForm()
	self.assertEqual(form.fields['name'].widget.attrs['id'], 'id_lesson_title')

    def test_form_renders_correct_fields(self):
	form = LessonEditForm()
        self.assertIn('id_lesson_title', form.as_p())
	self.assertIn('id_course', form.as_p())
	self.assertIn('id_abstract', form.as_p())
