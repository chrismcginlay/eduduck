"""
Unit tests for courses models
"""

import json
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from profile.models import Profile

from lesson.models import Lesson
from ..models import Course


class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

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
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('hank', 'hank@example.com', 'hankdo')
        self.user2.is_active = True
        self.user2.save()
        self.profile1 = self.user1.profile
        self.profile1.accepted_terms = True
        self.profile1.signature_line = 'Learning stuff'
        self.profile1.user_tz = "Europe/Rome"
        self.profile1.save()
        self.profile2 = self.user2.profile
        self.profile2.accepted_terms = True
        self.profile2.signature_line = 'Tieing knots'
        self.profile2.user_tz = 'Atlantic/St_Helena'
        self.profile2.save()

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
            
