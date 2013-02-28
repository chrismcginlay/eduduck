"""
Unit tests for Interaction app
"""

from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import (Course)
from .models import UserCourse

import pdb

class UserCourseModelTests(TestCase):
    """Test models user interaction with courses"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 'Basic',
                   'course_credits': 30,
                   }
                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        
    def test_checkrep(self):
        """Test the internal representation checker"""
        
        self.assert_(self.uc._checkrep(), "New registration checkrep failed")
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up error state")        
        self.uc.withdrawn=False
        self.uc.completed=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up error state")
        self.uc.completed=False
        self.uc.active=False
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up error state")
        self.uc.active=True
        self.uc.completed=True
        self.uc.withdrawn=False
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up mutually exclusive states")
        self.uc.active=True
        self.uc.completed=False
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up mutually exclusive states")
        self.uc.active=False
        self.uc.completed=True
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up mutually exclusive states")
        self.uc.active=True
        self.uc.completed=True
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up mutually exclusive states")

        
    def test_register(self):
        """Test that creating new row works"""
        
        self.uc = UserCourse(course=self.course1, user=self.user1).save()
        self.assert_(self.uc.pk, "Failed to create new db entry")
        self.assert_(self.uc._checkrep(), "_checkrep failed")

        
    
        