"""
Unit tests for Interaction app
"""

from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import (Course)

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
        
    def test_register(self):
        """Test that registration works"""
        
    
        