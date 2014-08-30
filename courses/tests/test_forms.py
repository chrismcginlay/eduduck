# Unit tests for course forms

from django.contrib.auth.models import User
from django.test import TestCase

from courses.forms import (
    COURSE_NAME_FIELD_REQUIRED_ERROR,
    COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
    CourseNameForm, 
    CourseFullForm,
)
from courses.models import Course

class CourseNameFormTest(TestCase):
    """ The homepage sports a quick course create form """
    
    def test_form_renders_course_name_input(self):
        form = CourseNameForm()
        self.assertIn('id_course_name', form.as_p())
        self.assertIn('A short name for the course', form.as_p())
        
class CourseFullFormTest(TestCase):
    """ The complete course form. Used to create and edit courses. """

    fixtures = [
        'auth_user.json', 
        'courses.json', 
    ]
    
    def test_fullform_has_correct_field_inputs(self):
        form = CourseFullForm()
        self.assertIn('<input id="id_code"', form.as_p())
        self.assertIn('<input id="id_name"', form.as_p())
        self.assertIn('id="id_abstract"', form.as_p())
        
    def test_fullform_validation_for_empty_field(self):
        form = CourseFullForm(data={'name':'', 'abstract':'', 'code':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [COURSE_NAME_FIELD_REQUIRED_ERROR],
            'abstract': [COURSE_ABSTRACT_FIELD_REQUIRED_ERROR],
        }
        self.assertEqual(form.errors, expected_errors)
    
    def test_fullform_allows_creation_of_course_with_no_course_code(self):
        person = User.objects.get(pk=1)
        form = CourseFullForm({
            'name': "Test Course",
            'abstract': "A course with no code. Should be fine.",
        })
        self.assertTrue(form.is_valid())
        form.instance.instructor = person
        form.instance.organiser = person
        form.save()
        
    def test_fullform_validation_with_course_name_too_long(self):
        form = CourseFullForm(data={
            'name': 'This name is far, far too long',
            'code': 'V4',
            'abstract': 'This abstract is fine.'
        })
        self.assertFalse(form.is_valid())
        expected_errors = { 'name': ['Ensure this value has at most 20 characters (it has 30).']}
        self.assertEqual(form.errors, expected_errors)
        
    def test_fullform_renders_course_from_database(self):
        course = Course.objects.get(pk=1)
        form = CourseFullForm(instance=course)
        self.assertIsInstance(form, CourseFullForm)
        self.assertEqual(form.instance, course)
        
    def test_fullform_allows_edit_of_instance_from_database(self):
        course = Course.objects.get(pk=1)
        form = CourseFullForm(instance=course)
        form.instance.name = "Fish paste"
        form.instance.save()
        course = Course.objects.get(pk=1)
        self.assertEqual(course.name, "Fish paste")
