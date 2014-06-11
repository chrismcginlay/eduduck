# Unit tests for course forms

from django.test import TestCase
from courses.forms import CourseNameForm, CourseFullForm

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
        