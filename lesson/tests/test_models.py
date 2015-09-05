from django.test import TestCase

from courses.models import Course
from ..models import Lesson

class LessonTests(TestCase):
    """ Test the models of the lesson app """
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
    ]
   
    def test__checkrep_True_case(self):
        lesson = Lesson.objects.get(pk=1) 
        self.assertTrue(lesson._checkrep())

    def test__checkrep_False_case(self):
        lesson = Lesson.objects.get(pk=1)
        lesson.name = ""
        self.assertFalse(lesson._checkrep())

    def test__required_field_Error_case(self):
        with self.assertRaises(ValueError):
            lesson = Lesson.objects.get(pk=1)
            lesson.course = None

    def test_verbose_names(self):
	""" Verbose names (which will be used in model forms) are correct """
	
        self.assertEqual(
            Lesson._meta.get_field('name').verbose_name, 'lesson title')
	 
    def test_get_next_when_next_exists(self):
        """ Should return the next lesson in the sequence of a course """

        first = Lesson.objects.get(pk=1)
        second = Lesson.objects.get(pk=2)
        self.assertEqual(first.get_next(), second)

    def test_get_next_when_at_end(self):
        """ At end of lessons, should return False """

        course = Course.objects.get(pk=1)
        ultimate = course.lesson_set.last()
        self.assertEqual(ultimate.get_next(), False)

    def test_get_prev_when_prev_exists(self):
        """ Should return the previous lesson in the sequence of a course """
        
        first = Lesson.objects.get(pk=1)
        second = Lesson.objects.get(pk=2)
        self.assertEqual(first, second.get_prev())

    def test_get_prev_when_at_start(self):

        course = Course.objects.get(pk=1)
        first = course.lesson_set.first()
        self.assertEqual(first.get_prev(), False)

    def test_get_absolute_url(self):
        """Lesson returns correct get_absolute_url"""

        lesson = Lesson.objects.get(pk=1)
        url = lesson.get_absolute_url()
        target = u"/courses/{0}/lesson/{1}/".format(lesson.course.pk,lesson.pk)
        self.assertEqual(target, url, "lesson URL error")

