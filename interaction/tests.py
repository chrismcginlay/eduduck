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

    course2_data = {'course_code': 'EDU03',
                   'course_name': 'The Coarse and The Hoarse',
                   'course_abstract': 'High volume swearing leading to loss of voice',
                   'course_organiser': 'Genghis Khan',
                   'course_level': 'Advanced',
                   'course_credits': 30,
                   }
                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        
    def test_checkrep(self):
        """Test the internal representation checker"""
        self.assert_(self.uc._checkrep(), "New registration checkrep failed")
        self.uc.active=False
        self.uc.completed=False
        self.uc.withdrawn=False
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up --- error state")
        self.uc.active=True
        self.uc.completed=True
        self.uc.withdrawn=False
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up AC- error state")
        self.uc.active=True
        self.uc.completed=False
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up A-W error state")
        self.uc.active=False
        self.uc.completed=True
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up -CW error state")
        self.uc.active=True
        self.uc.completed=True
        self.uc.withdrawn=True
        self.assertFalse(self.uc._checkrep(), "Checkrep didn't pick up ACW error state")

    def test_usercourse_create(self):
        """Test creating new row"""
        
        pdb.set_trace()
        self.uc = UserCourse(course=self.course2, user=self.user1)
        self.uc.save()
        self.assert_(self.uc.pk, "Failed to create new db entry")
        self.assert_(self.uc._checkrep(), "_checkrep failed")

        
    
        