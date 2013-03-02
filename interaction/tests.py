"""
Unit tests for Interaction app
"""

import datetime

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
    course3_data = {'course_code': 'EDU04',
                   'course_name': 'Pie Eating',
                   'course_abstract': 'Gut Busting leads to Butt Gusting',
                   'course_organiser': 'Phat Bstard',
                   'course_level': 'Horizontal',
                   'course_credits': 30,
                   }
                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.course3 = Course(**self.course3_data)
        self.course3.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        self.uc2 = UserCourse(course=self.course2, user=self.user1)
        self.uc2.save()
        self.uc3 = UserCourse(course=self.course3, user=self.user1)
        self.uc3.save()
        
    def test_checkrep(self):
        """Test the internal representation checker with course 1"""
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
        #put the flags back to normal
        self.uc.active = True
        self.uc.withdrawn = False
        self.uc.completed = False

    def test_usercourse_create(self):
        """Test creating new row with course 2"""
        
        self.assert_(self.uc2.pk, "Failed to create new db entry")
        self.assert_(self.uc2._checkrep(), "_checkrep failed")

    def test_hist2list(self):
        """Test conversion of JSON encoded history to tuple list with course 3"""
       
        self.uc3.withdraw()
        self.uc3.reopen()
        self.uc3.complete()
        
        h2l_output = self.uc3.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, "Should be a datetime")
            self.assertIsInstance(row[1], str, "Action should be a string")
            
        #Now check the history messages in reverse order.
        last = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Action should be DEACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'COMPLETION', "Action should be COMPLETION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Action should be ACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REOPENING', "Action should be REOPENING")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Action should be DEACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'WITHDRAWAL', "Action should be WITHDRAWAL")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Action should be ACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REGISTRATION', "Action should be REGISTRATION")
        
    def test_withdraw(self):
        """Test the course withdraw method"""
        
        self.uc.withdraw()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'WITHDRAWAL', "Wrong action in history")
        self.assertEqual(self.uc.active, False, "Should not be active")
        self.assertEqual(self.uc.withdrawn, True, "Should be withdrawn")
        self.assertEqual(self.uc.completed, False, "Should not be completed")
        
    def test_reopen(self):
        """Test the course reopen method"""

        self.uc.complete() 
        self.uc.reopen()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'REOPENING', "Wrong action in history")
        self.assertEqual(self.uc.active, True, "Should be active")
        self.assertEqual(self.uc.withdrawn, False, "Should not be withdrawn")
        self.assertEqual(self.uc.completed, False, "Should not be completed")
        
    def test_complete(self):
        """Test the course complete method"""
        
        self.uc.complete()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'COMPLETION', "Wrong action in history")
        self.assertEqual(self.uc.active, False, "Should not be active")
        self.assertEqual(self.uc.withdrawn, False, "Should not be withdrawn")
        self.assertEqual(self.uc.completed, True, "Should be completed")
    
    def test___str__(self):
        """Test that the desired info is in the unicode method"""
        s = self.uc3.__str__()
        self.assertIn(self.uc3.user.username, s, "The username should be in the unicode")
        self.assertIn(self.uc3.course.course_name, s, "The course_name should be in the unicode")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""
        unicod = self.uc3.__unicode__()
        s = u"UC:%s, User:%s, Course:%s" % \
            (self.uc3.pk, self.uc3.user.pk, self.uc3.course.pk)
        self.assertEqual(unicod, s, "Unicode output failure")

        
    def test_get_absolute_url(self):
        """Test the correct url is returned"""
        
        url = self.uc3.get_absolute_url()
        u = self.uc3.user.pk
        c = self.uc3.course.pk
        s = "/interaction/user/%s/course/%s/"% (u,c)
        self.assertEqual(s, url, "URL error")
        