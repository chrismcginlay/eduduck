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
    
    def test_smoke(self):
        self.fail("smoke test unit")
