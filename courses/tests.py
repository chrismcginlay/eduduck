"""
Unit tests for Courses app
"""

from django.test import TestCase
from django.contrib.auth.models import User

from bio.models import Bio

from interaction.models import UserCourse
from .models import (Course, Lesson, Video, Attachment, UserProfile_Lesson,
                     LearningIntention, SuccessCriterion, LearningOutcome,)

import pdb

class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

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
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': '5',
                   'course_credits': 20,
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
        self.user1.save()
        self.bio1 = Bio.objects.get(user_id=1)
        self.bio1.accepted_terms = True
        self.bio1.signature_line = 'Learning stuff'
        self.bio1.save()
       
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    li_text = "Practise")
        self.learningintention1.save()                                            
        self.successcriterion1 = SuccessCriterion(
            learning_intention = self.learningintention1, 
            criterion_text = "Choose"
        )
        self.successcriterion1.save()                                          
        self.learningoutcome1 = LearningOutcome(
            learning_intention = self.learningintention1, 
            lo_text = "Calculate"
        )
        self.learningoutcome1.save()                                        
        
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

    def test_bio_create(self):
        """Bio instance attributes are created OK"""
        self.assertEqual(self.bio1.user, self.user1)
        #self.assertEqual(self.bio1.lessons.all()[0], self.lesson1)
        #self.assertEqual(self.bio1.registered_courses, self.registered_courses)
          
    def test_learningIntention_create(self):
        """LearningIntention instance attributes are created OK"""
        self.assertEqual(self.learningintention1.lesson, self.lesson1)
        self.assertEqual(self.learningintention1.li_text, "Practise")
    
    def test_successCriterion_create(self):
        """SuccessCriterion instance attributes are created OK"""
        self.assertEqual(self.successcriterion1.learning_intention, self.learningintention1)
        self.assertEqual(self.successcriterion1.criterion_text, "Choose")
        
    def test_learningOutcome_create(self):
        """LearningOutcome instance attributes are created OK"""
        self.assertEqual(self.learningoutcome1.learning_intention, self.learningintention1)
        self.assertEqual(self.learningoutcome1.lo_text, "Calculate")
    
class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 'basic',
                   'course_credits': 30,
                   }
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': '5',
                   'course_credits': 20,
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
        self.user1.save()
        self.bio1 = Bio.objects.get(user_id=1)
        self.bio1.accepted_terms = True
        self.bio1.signature_line = 'Learning stuff'
        self.bio1.save()     
#        self.bio1.registered_courses.add(self.course1)
        
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    li_text = "Practise")
        self.learningintention1.save()
        self.successcriterion1 = SuccessCriterion(
            learning_intention = self.learningintention1, 
            criterion_text = "Choose"
        )
        self.successcriterion1.save()
        self.learningoutcome1 = LearningOutcome(
            learning_intention = self.learningintention1, 
            lo_text = "Calculate"
        )
        self.learningoutcome1.save()
        
    def test_course_index(self):
        """Check course index page loads OK and has correct variables"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        self.assertTrue(x in response.context for x in ['course_list', 
                                                        'course_count'])
            
    def test_course_single_auth(self):
        """Check course page loads for authorised user"""

        #First, when the user is not registered on course
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertIn('course', response.context, \
            "Missing template var: course")
        self.assertNotIn('uc', response.context, \
            "Missing template var: uc")
        self.assertNotIn('history', response.context, \
            "Missing template var: history")       
        self.assertEqual('auth_noreg', response.context['status'], \
            "Registration status should be auth_noreg")
            
        #Register the user and repeat
        uc = UserCourse(user=self.user1, course=self.course1)
        uc.save()
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertIn('course', response.context, \
            "Missing template var: course")
        self.assertIn('uc', response.context, \
            "Missing template var: uc")
        self.assertIn('history', response.context, \
            "Missing template var: history")
        self.assertEqual('auth_reg', response.context['status'], \
            "Registration status should be auth_reg")
        self.assertEqual(response.context['course'].pk, 1)
        
        #check 404 for non-existent course
        response = self.client.get('/courses/5/')
        self.assertEqual(response.status_code, 404)
        
        #check redirect for trailing slash
        response = self.client.get('/courses/5')
        self.assertEqual(response.status_code, 301)

    def test_course_single_unauth(self):        
        """Check individual course page loads for unauth user"""

        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertIn('course', response.context, \
            "Missing template var: course")
        self.assertNotIn('uc', response.context, \
            "Missing template var: uc")
        self.assertNotIn('history', response.context, \
            "Missing template var: history")
        self.assertEqual('anon', response.context['status'], \
            "Registration status should be anon")
        self.assertEqual(response.context['course'].pk, 1)   
        
    def test_course_lesson(self):
        """Test view of single lesson"""
        response = self.client.get('/courses/1/lesson/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['course', 'lesson', 'user_lessons'])
                                                        
    def test_learning_intention(self):
        """Test view of a single learning intention"""
        response = self.client.get('/lesson/1/lint/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['lesson_id', 'lesson_intention_id'])
            
