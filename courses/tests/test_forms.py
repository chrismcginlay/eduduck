# Unit tests for course forms

from django.test import TestCase
from courses.forms import (
    NAME_FIELD_REQUIRED_ERROR,
    CODE_FIELD_REQUIRED_ERROR,
    ABSTRACT_FIELD_REQUIRED_ERROR,
    CourseNameForm, 
    CourseFullForm,
)

class CourseNameFormTest(TestCase):
    """ The homepage sports a quick course create form """
    
    def test_form_renders_course_name_input(self):
        form = CourseNameForm()
        self.assertIn('id_course_create', form.as_p())
        self.assertIn('A short name for the course', form.as_p())
        
class CourseFullFormTest(TestCase):
    """ The complete course create form """
    
    def test_fullform_has_correct_field_inputs(self):
        form = CourseFullForm()
        self.assertIn('<input id="id_code"', form.as_p())
        self.assertIn('<input id="id_name"', form.as_p())
        self.assertIn('id="id_abstract"', form.as_p())
        
    def test_form_validation_for_empty_field(self):
        form = CourseFullForm(data={'name':'', 'abstract':'', 'code':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [NAME_FIELD_REQUIRED_ERROR],
            'abstract': [ABSTRACT_FIELD_REQUIRED_ERROR],
            'code': [CODE_FIELD_REQUIRED_ERROR],
        }
        self.assertEqual(form.errors, expected_errors)