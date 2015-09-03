#courses/tests/test_models.py
import json
from datetime import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from checkout.models import PricedItem
from lesson.models import Lesson
from profile.models import Profile

from factories import UserFactory, CourseFactory
from ..models import Course


class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

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

        # Prepare some courses
        self.course1 = CourseFactory(
            code = u'EDU02',
            name = u'A Course of Leeches',
            abstract = u'Learn practical benefits of leeches',
            organiser = self.user1,
            instructor = self.user2,
        )
    
        self.course2 = CourseFactory(
            code = u'FBR9',
            name = u'Basic Knitting',
            abstract = u'Casting on',
            organiser = self.user1,
            instructor = self.user2,
        )

        self.course3 = CourseFactory(
            name = u'Public Speaking',
            abstract = u'Talking in public',
            organiser = self.user1,
            instructor = self.user2,
        )

    def test___unicode__(self):
        uni_name = self.course1.__unicode__()
        self.assertEqual(uni_name, u'A Course of Leeches')
 
    def test_course_create(self):
        """A course can be created and saved"""
        self.assertEqual(self.course1.pk, 1)
 
    def test_cannot_create_invalid_course(self):
        with self.assertRaises(IntegrityError):
            invalid_course = Course()
            invalid_course.save()
        
    def test_model_has_meta_permissions(self):
        perms = Course._meta.permissions
        self.assertTrue('study_course' in (perm[0] for perm in perms))

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
   
    def test_new_course_has_PricedItem_created(self):
        new_course = CourseFactory(
            code = u'TEST1',
            name = u'test course',
            abstract = u'see the PricedItem instance is created',
            organiser = self.user1,
            instructor = self.user1
        )
        pitem = PricedItem.objects.get(object_id = new_course.id)
 
