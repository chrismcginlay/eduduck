"""
Unit tests for Interaction views
"""

from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from courses.models import (Course, Lesson)
from ..models import UserCourse, UserLesson

import pdb

class UserCourseViewTests(TestCase):
    """Test usercourse views"""

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
    course4_data = {'course_code': 'EDU05',
                   'course_name': 'Golf',
                   'course_abstract': 'The Contact Sport',
                   'course_organiser': 'Ahfu Dent',
                   'course_level': 'Medium',
                   'course_credits': 30,
                   }                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.course3 = Course(**self.course3_data)
        self.course3.save()
        self.course4 = Course(**self.course4_data)
        self.course4.save()
        
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        self.uc2 = UserCourse(course=self.course2, user=self.user1)
        self.uc2.save()
        self.uc3 = UserCourse(course=self.course3, user=self.user1)
        self.uc3.save()
        
    def test_usercourse_single(self):
        """Test that the view contains the correct context vars"""
        
        #Not logged in
        response = self.client.get('/interaction/user/1/course/1/')
        self.assertEqual(response.status_code, 302)
        
        #Now logged in
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/interaction/user/1/course/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['uc', 'history'])
            
        #non existent record
        response = self.client.get('/interaction/user/1/course/4/')
        self.assertEqual(response.status_code, 404)
      
      
class UserLessonViewTests(TestCase):
    """Test userlesson views"""
    
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
        self.lesson1 = Lesson(lesson_code="L1", 
                      lesson_name="Test Lesson 1",
                      course = self.course1)
        self.lesson1.save()
        self.ul = UserLesson(user=self.user1, lesson=self.lesson1)
        self.ul.save()
        
    def test_userlesson_single(self):
        """View contains correct context variables"""
        
        #Not logged in
        response = self.client.get('/interaction/user/1/lesson/1/')
        self.assertEqual(response.status_code, 302)
        
        #Now logged in
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/interaction/user/1/lesson/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['ul', 'history'])
            
        #non existent record
        response = self.client.get('/interaction/user/1/lesson/4/')
        self.assertEqual(response.status_code, 404)
        