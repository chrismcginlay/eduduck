#courses/tests/test_models.py
import json
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from lesson.models import Lesson
from profile.models import Profile

from factories import UserFactory, CourseFactory
from ..models import Course


class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

    course1_data = {
        'code': 'EDU02',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
    }
    course2_data = {
        'code': 'FBR9',
        'name': 'Basic Knitting',
        'abstract': 'Casting on',
    }
    course3_data = {
        'name': 'Public Speaking',
        'abstract': 'Talking in public',
    }
    lesson1_data = {
        'name': 'Introduction to Music',
        'abstract': 'A summary of what we cover',
    }
        
    def setUp(self):
        # Prepare two users for each test, Bertie and Hank
        self.user1 = UserFactory(
            username = 'bertie',
            email = 'bertie@example.com',
            password = 'bertword'
        )
        self.user1.save()
        self.user1.profile.user_tz = "Europe/Rome" # vary from factory default
        self.user1.profile.save()

        self.user2 = UserFactory(
            username = 'hank',
            email = 'hank@example.com', 
            password = 'hankdo'
        )
        self.user2.save()
        self.user2.profile.signature_line = 'Tieing knots'
        self.user2.profile.user_tz = 'Atlantic/St_Helena'
        self.user2.profile.save()

        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user2
        self.course1.save()

        self.course2 = Course(**self.course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user2
        self.course2.save()

        self.course3 = Course(**self.course3_data)
        self.course3.organiser = self.user1
        self.course3.instructor = self.user2
        self.course3.save()

        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()

    def test_course_create(self):
        """Course instance attributes are created OK"""
        for key,val in self.course1_data.items():
            self.assertEqual(self.course1.__dict__[key], val)
    
    def test_cannot_create_invalid_course(self):
        with self.assertRaises(AssertionError):
            invalid_course = Course()
            invalid_course.save()
            invalid_course.full_clean()
        
    def test_can_create_a_course_without_course_code(self):
        """ Course code is optional """
        new_course = Course.objects.create(
            name = "Test Course",
            abstract = "This course has no code. Should be fine",
            organiser = self.user1,
            instructor = self.user1,
        )
        new_course.save()
        
    def test_course_get_absolute_url(self):
        """Course returns correct get_absolute_url"""
        
        url = self.course1.get_absolute_url()
        target = u"/courses/%s/" % self.course1.pk
        self.assertEqual(target, url, "course URL error")
    
    def test_lesson_get_absolute_url(self):
        """Lesson returns correct get_absolute_url"""

        url = self.lesson1.get_absolute_url()
        target = u"/courses/{0}/lesson/{1}/".format(self.lesson1.course.pk,self.lesson1.pk)
        self.assertEqual(target, url, "lesson URL error")

    def test_lesson_create(self):
        """Lesson instance attributes are created OK"""
        for key,val in self.lesson1_data.items():
            self.assertEqual(self.lesson1.__dict__[key], val)
        self.assertEqual(self.lesson1.course, self.course1)
            
