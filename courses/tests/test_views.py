"""
Unit tests for courses views
"""

import json
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from bio.models import Bio

from interaction.models import UserCourse
from outcome.models import LearningIntention, LearningIntentionDetail
from attachment.models import Attachment

from ..models import Course, Lesson, Video

class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   'level': 'basic',
                   'credits': 30,
                   }
    course2_data = {'code': 'FBR9',
                   'name': 'Basic Knitting',
                   'abstract': 'Casting on',
                   'level': '5',
                   'credits': 20,
                   }  
    course3_data = {'code': 'G3',
                   'name': 'Nut Bagging',
                   'abstract': 'Put the nuts in the bag',
                   'level': '4',
                   'credits': 42,
                   }
    lesson1_data = {'code': 'B1',
                    'name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    lesson2_data = {'code': 'B2',
                    'name': 'Stuff',
                    'abstract': 'Not a lot',
                   }
    video1_data = {'code': 'MV2',
                   'url': 'http://youtu.be/LIM--jfnKeU',
                   'name': 'Music introduction',
                  }
    attachment1_data = {'code': 'DOC1',
                        'name': 'Reading List',
                        'desc': 'Useful stuff you might need',
                        'seq': 3,
                        'attachment': 'empty_attachment_test.txt',
                        }                   
    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('hank', 'hank@example.com', 'hankdo')
        self.user2.is_active = True
        self.user2.save()
        self.bio1 = self.user1.bio
        self.bio1.accepted_terms = True
        self.bio1.signature_line = 'Learning stuff'
        self.bio1.user_tz = "Europe/Rome"
        self.bio1.save()
        self.bio2 = self.user2.bio
        self.bio2.accepted_terms = True
        self.bio2.signature_line = 'Tieing knots'
        self.bio2.user_tz = 'Atlantic/St_Helena'
        self.bio2.save()

        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()

        self.course2 = Course(**self.course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user2
        self.course2.save()

        self.course3 = Course(**self.course3_data)
        self.course3.organiser = self.user2
        self.course3.instructor = self.user2
        self.course3.save()

        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.lesson2 = Lesson(course=self.course3, **self.lesson2_data)
        self.lesson2.save()
        self.video1 = Video(course=self.course1, **self.video1_data)
        self.video1.save()
        self.video2 = Video(lesson=self.lesson1, **self.video1_data)
        self.video2.save()
        self.attachment1 = Attachment(course=self.course1, 
                                      **self.attachment1_data)
        self.attachment1.save()
        
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    text = "Practise")
        self.learningintention1.save()
        self.learningintentiondetail1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Choose",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.learningintentiondetail1.save()
        self.learningintentiondetail2 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Calculate",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.learningintentiondetail2.save()
        
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
        #check template variables present as approp
        self.assertIn('course', response.context, \
            "Missing template var: course")
        self.assertNotIn('uc', response.context, \
            "Missing template var: uc")
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertNotIn('history', response.context, \
            " Template var should not be there: history")       
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
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
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

        #see that unregistered user get the register button
        response = self.client.get('/courses/2/')
        self.assertIn('course_register', response.content)
        self.assertEqual(response.context['status'], 'auth_noreg')
        
        #see that registration button works (user registers)
        response = self.client.post('/courses/2/', {'course_register':'Register'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertEqual(response.context['course'], self.course2)
        self.assertIn('course_complete', response.content)
        self.assertIn('course_withdraw', response.content)
        self.assertEqual(response.context['uc'].active, True)        
        
        #see that a registered user can withdraw
        response = self.client.post('/courses/2/', {'course_withdraw':'Withdraw'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_reopen', response.content)
        self.assertEqual(response.context['uc'].active, False)        
        self.assertEqual(response.context['uc'].withdrawn, True)        
        
        #see that a withdrawn user can reopen
        response = self.client.post('/courses/2/', {'course_reopen':'Re-open'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_complete', response.content)
        self.assertIn('course_withdraw', response.content)
        self.assertEqual(response.context['uc'].active, True)
        self.assertEqual(response.context['uc'].withdrawn, False)                
        
        #see that a registered user can complete
        response = self.client.post('/courses/2/', {'course_complete':'Complete'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_reopen', response.content)
        self.assertEqual(response.context['uc'].active, False)                
        self.assertEqual(response.context['uc'].completed, True)        
        
        
    def test_course_single_unauth(self):        
        """Check individual course page loads for unauth user"""

        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertIn('course', response.context, \
            "Missing template var: course")
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertNotIn('uc', response.context, \
            "Missing template var: uc")
        self.assertNotIn('history', response.context, \
            "Missing template var: history")
        self.assertEqual('anon', response.context['status'], \
            "Registration status should be anon")
        self.assertEqual(response.context['course'].pk, 1)   
        

    def test_course_lesson_unauth(self):
        """Test view of single lesson for unauthenticated user"""

        self.client.logout()        
        response = self.client.get('/courses/1/lesson/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['course', 'lesson', 'ul', 'attachments',
                      'history', 'learning_intentions'])
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - unauthenticate")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - unauthenticated")                 

    def test_course_lesson_auth(self):
        """Test view of single lesson for authenticated user"""

        self.client.login(username='bertie', password='bertword')        

        #First for user who is registered on course
        uc = UserCourse(course=self.course1, user=self.user1)
        uc.save()
        c = self.course1.pk
        url = '/courses/{0}/lesson/1/'.format(c)
        response = self.client.get(url)

        import pdb; pdb.set_trace()
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.status_code, 200)
        hist = response.context['history'].pop()
        self.assertIsInstance(hist[0], datetime, 
                         "Problem with lesson history timestamp")
        self.assertEqual(hist[1], 'VISITING', 
                         "Problem with lesson history activity")
                         
        self.assertNotEqual(response.context['ul'], None, 
                         "There should be a userlesson - authenticated")                 
        #see that lesson complete button works 
        response = self.client.post('/courses/1/lesson/1/', {'lesson_complete':'Complete'})
        self.assertIn('lesson_reopen', response.content)
        self.assertEqual(response.context['ul'].completed, True) 
                
        #see that lesson reopen button works 
        response = self.client.post('/courses/1/lesson/1/', {'lesson_reopen':'Re-open'})
        self.assertIn('lesson_complete', response.content)
        self.assertEqual(response.context['ul'].completed, False)        
                         
        #then check context for user not registered on course
        response = self.client.get('/courses/3/lesson/2/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - unregistered")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - unregistered")                 
