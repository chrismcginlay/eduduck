from django.test import TestCase

from ..forms import (
    LESSON_NAME_FIELD_REQUIRED_ERROR,
    LESSON_ABSTRACT_FIELD_REQUIRED_ERROR,
    LessonEditForm
) 
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

    def test_form_has_correct_error_messages(self):
        form = LessonEditForm(data={'name':'', 'abstract':'', 'code':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [LESSON_NAME_FIELD_REQUIRED_ERROR],
            'abstract': [LESSON_ABSTRACT_FIELD_REQUIRED_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)
    
