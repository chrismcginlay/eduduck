from django.test import TestCase

from ..forms import (
    LESSON_NAME_FIELD_REQUIRED_ERROR,
    LESSON_ABSTRACT_FIELD_REQUIRED_ERROR,
    LessonEditForm
) 
from ..models import Lesson

class LessonFormTests(TestCase):
    """ Test the form used in formsets during course edit """
    
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
        form = LessonEditForm(
            data={'course':u'1', 'name':'', 'abstract':'', 'code':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [LESSON_NAME_FIELD_REQUIRED_ERROR],
            'abstract': [LESSON_ABSTRACT_FIELD_REQUIRED_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)

class LessonFullFormTests(TestCase):
    """ Test the full lesson edit form """

    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lesson.json',
    ]
    
    def test_fullform_has_correct_field_inputs(self):
        form = LessonFullForm()
        self.assertIn('<input id="id_name"', form.as_p())
        self.assertIn('id="id_abstract"', form.as_p())
        
    def test_fullform_validation_for_empty_field(self):
        form = LessonFullForm(data={'name':'', 'abstract':'',})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [LESSON_NAME_FIELD_REQUIRED_ERROR],
            'abstract': [LESSON_ABSTRACT_FIELD_REQUIRED_ERROR],
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
        
    def test_fullform_validation_and_save_with_valid_input(self):
        form = CourseFullForm(data={
            'name': 'How to Throw a Wellington Boot.',
            'abstract': 'This abstract is fine.'
        })
        self.assertTrue(form.is_valid())
        form.instance.course = Courses.objects.get(pk=1)
        form.save()
        
    def test_fullform_renders_lesson_from_database(self):
        lesson = Lesson.objects.get(pk=1)
        form = LessonFullForm(instance=lesson)
        self.assertIsInstance(form, LessonFullForm)
        self.assertEqual(form.instance, lesson)
        
    def test_fullform_allows_edit_of_instance_from_database(self):
        lesson = Lesson.objects.get(pk=1)
        form = LessonFullForm(instance=lesson)
        form.instance.name = "Fish paste"
        form.instance.abstract = "Spread on bread"
        assert(form.instance.lesson)
        form.instance.save()
 
