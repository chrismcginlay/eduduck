"""
Unit tests for Courses app
"""

from django.test import TestCase
from django.contrib.auth.models import User

from .models import (Course, Lesson, Video, Attachment, 
                     UserProfile, UserProfile_Lesson)

class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': 5,
                   'course_credits': -20,
                   }
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    video1_data = {'video_code': 'MV2',
                   'url': 'http://youtu.be/LIM--jfnKeU',
                   'video_name': 'Music introduction',
                  }
    attachment1_data = {'att_code': 'DOC1',
                        'att_name': 'Reading List',
                        'att_desc': 'Useful stuff you might need',
                        'att_seq': 3,
                        'attachment': 'empty_attachment_test.txt',
                        }
    userprofile_lesson1_data = {'mark_complete': False,
                               'date_complete': '2013-01-19',}
    
    
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.video1 = Video(course=self.course1, **self.video1_data)
        self.video1.save()
        self.video2 = Video(lesson=self.lesson1, **self.video1_data)
        self.video2.save()
        self.attachment1 = Attachment(course=self.course1, 
                                      **self.attachment1_data)
        self.attachment1.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.userprofile1 = UserProfile.objects.get(user_id=1)
        self.userprofile1.accepted_terms = True
        self.userprofile1.signature_line = 'Learning stuff'
        self.userprofile1.save()     
        self.userprofile1.registered_courses.add(self.course1)
        self.userprofile1.save()
        self.userprofile_lesson1 = UserProfile_Lesson(
            userprofile = self.userprofile1,
            lesson = self.lesson1,
            date_complete = '2013-01-19',
            mark_complete = False,
        )
        self.userprofile_lesson1.save()
        
    def test_course_create(self):
        """Course instance attributes are created OK"""
        for key,val in self.course1_data.items():
            self.assertEqual(self.course1.__dict__[key], val)
    
    def test_lesson_create(self):
        """Lesson instance attributes are created OK"""
        for key,val in self.lesson1_data.items():
            self.assertEqual(self.lesson1.__dict__[key], val)
        self.assertEqual(self.lesson1.course, self.course1)
            
    def test_video_create(self):
        """Video instance attributes are created OK"""
        #Associated with course
        for key,val in self.video1_data.items():
            self.assertEqual(self.video1.__dict__[key], val)
        self.assertEqual(self.video1.course, self.course1)
            
        #Associated with lesson
        for key,val in self.video1_data.items():
            self.assertEqual(self.video2.__dict__[key], val)
        self.assertEqual(self.video2.lesson, self.lesson1)
            
    def test_attachment_create(self):
        """Attachment instance attributes are created OK"""
        for key,val in self.attachment1_data.items():
            self.assertEqual(self.attachment1.__dict__[key], val)   
        self.assertEqual(self.attachment1.course, self.course1)

    def test_userProfile_create(self):
        """UserProfile instance attributes are created OK"""
        self.assertEqual(self.userprofile1.user, self.user1)
        self.assertEqual(self.userprofile1.lessons.all()[0], self.lesson1)
        #self.assertEqual(self.userprofile1.registered_courses, self.registered_courses)
        
    def test_userProfile_Lesson_create(self):
        """UserProfile_Lesson attributes are created OK"""
        for key,val in self.userprofile_lesson1_data.items():
            self.assertEqual(self.userprofile_lesson1.__dict__[key], val)        
        self.assertEqual(self.userprofile_lesson1.userprofile, self.userprofile1)
        self.assertEqual(self.userprofile_lesson1.lesson, self.lesson1)
    
    
class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': 5,
                   'course_credits': -20,
                   }  
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    video1_data = {'video_code': 'MV2',
                   'url': 'http://youtu.be/LIM--jfnKeU',
                   'video_name': 'Music introduction',
                  }
    attachment1_data = {'att_code': 'DOC1',
                        'att_name': 'Reading List',
                        'att_desc': 'Useful stuff you might need',
                        'att_seq': 3,
                        'attachment': 'empty_attachment_test.txt',
                        }                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.video1 = Video(course=self.course1, **self.video1_data)
        self.video1.save()
        self.video2 = Video(lesson=self.lesson1, **self.video1_data)
        self.video2.save()
        self.attachment1 = Attachment(course=self.course1, 
                                      **self.attachment1_data)
        self.attachment1.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.set_password('bertword')
        self.user1.save()
        self.userprofile1 = UserProfile.objects.get(user_id=1)
        self.userprofile1.accepted_terms = True
        self.userprofile1.signature_line = 'Learning stuff'
        self.userprofile1.save()     
        self.userprofile1.registered_courses.add(self.course1)
        self.userprofile1.save()
        self.userprofile_lesson1 = UserProfile_Lesson(
            userprofile = self.userprofile1,
            lesson = self.lesson1,
            date_complete = '2013-01-19',
            mark_complete = False,
        )
        self.userprofile_lesson1.save()
    def test_course_index(self):
        """Check course index page loads OK and has correct variables"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        self.assertTrue(x in response.context for x in ['course_list', 
                                                        'course_count'])
            
    def test_course_single(self):
        """Check individual course page loads"""
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertTrue('course' in response.context)
        self.assertEqual(response.context['course'].pk, 1)
        
        #check 404 for non-existent course
        response = self.client.get('/courses/5/')
        self.assertEqual(response.status_code, 404)
        
        #check redirect for trailing slash
        response = self.client.get('/courses/5')
        self.assertEqual(response.status_code, 301)
        
    def test_course_lesson(self):
        """Test view of single lesson"""
        response = self.client.get('/courses/1/lesson/1/')
        #not logged in, redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(x in response.context for x in ['course', 
                                                        'lesson', 
                                                        'user_lessons'])
        #log in and test

        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/courses/1/lesson/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context for x in ['course', 
                                                        'lesson', 
                                                        'user_lessons'])
