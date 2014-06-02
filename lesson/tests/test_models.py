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
    
    def test_get_next(self):
        """ Should return the next lesson in the sequence of a course """

        first = Lesson.objects.get(pk=1)
        second = Lesson.objects.get(pk=2)
        self.assertEqual(first.get_next(), second)

    def test_get_next(self):
        """ Should return the previous lesson in the sequence of a course """
        
        first = Lesson.objects.get(pk=1)
        second = Lesson.objects.get(pk=2)
        self.assertEqual(first, second.get_prev())
        