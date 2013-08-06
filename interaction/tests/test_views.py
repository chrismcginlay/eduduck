"""
Unit tests for Interaction views
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from courses.models import Course, Lesson
from outcome.models import LearningIntention, LearningIntentionDetail
from attachment.models import Attachment
from ..models import (UserCourse, 
                      UserLesson, 
                      UserLearningIntention,
                      UserLearningIntentionDetail,
                      UserAttachment)

class UserCourseViewTests(TestCase):
    """Test usercourse views"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   'level': 'Basic',
                   'credits': 30,
                   }

    course2_data = {'code': 'EDU03',
                   'name': 'The Coarse and The Hoarse',
                   'abstract': 'High volume swearing leading to loss of voice',
                   'level': 'Advanced',
                   'credits': 30,
                   }
    course3_data = {'code': 'EDU04',
                   'name': 'Pie Eating',
                   'abstract': 'Gut Busting leads to Butt Gusting',
                   'level': 'Horizontal',
                   'credits': 30,
                   }
    course4_data = {'code': 'EDU05',
                   'name': 'Golf',
                   'abstract': 'The Contact Sport',
                   'level': 'Medium',
                   'credits': 30,
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

        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.user4 = User.objects.create_user('James Maxwell', 'em@c', 'pdq')
        self.user4.is_active = True
        self.user4.save()

        self.course1.organiser = self.user2
        self.course1.instructor = self.user2
        self.course2.organiser = self.user3
        self.course2.instructor = self.user2
        self.course3.organiser = self.user4
        self.course3.instructor = self.user4
        self.course4.organiser = self.user2
        self.course4.instructor = self.user3
        self.course1.save()
        self.course2.save()
        self.course3.save()
        self.course4.save()

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
    
    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   'level': 'Basic',
                   'credits': 30,
                   }

    course2_data = {'code': 'EDU03',
                   'name': 'The Coarse and The Hoarse',
                   'abstract': 'High volume swearing leading to loss of voice',
                   'level': 'Advanced',
                   'credits': 30,
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

        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.user4 = User.objects.create_user('James Maxwell', 'em@c', 'pdq')
        self.user4.is_active = True
        self.user4.save()
        
        self.course1.organiser = self.user2
        self.course1.instructor = self.user2
        self.course2.organiser = self.user3
        self.course2.instructor = self.user2
        self.course1.save()
        self.course2.save()

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
        
class UserLearningIntentionViewTests(TestCase):
    """Test views for learning intention interaction"""

    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   'level': 'Basic',
                   'credits': 30,
                   }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()    
        self.course1 = Course(**self.course1_data)
        self.course1.save() 

        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()

        self.course1.organiser = self.user2
        self.course1.instructor = self.user2
        self.course1.save()

        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        self.lesson = Lesson(lesson_code="L1", 
                      lesson_name="Test Lesson 1",
                      course = self.course1)
        self.lesson.save() 
        self.li = LearningIntention(lesson=self.lesson, li_text="Intend...")
        self.li.save()
        self.uli = UserLearningIntention(user=self.user1, 
                                         learning_intention = self.li)
        self.lid1 = LearningIntentionDetail(
            learning_intention=self.li, 
            lid_text ="LID A",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid2 = LearningIntentionDetail(
            learning_intention=self.li, 
            lid_text ="LID B",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid3 = LearningIntentionDetail(
            learning_intention=self.li, 
            lid_text ="LID C",
            lid_type=LearningIntentionDetail.LEARNING_OUTCOME)
        self.lid1.save()
        self.lid2.save()
        self.lid3.save()   
        self.ulid1 = UserLearningIntentionDetail(user=self.user1,
                                    learning_intention_detail=self.lid1)
        self.ulid1.save()    
        self.ulid2 = UserLearningIntentionDetail(user=self.user1,
                                    learning_intention_detail=self.lid2)
        self.ulid2.save()
        self.ulid3 = UserLearningIntentionDetail(user=self.user1,
                                    learning_intention_detail=self.lid3)
        self.ulid3.save()         
            
""" TODO Not working test of ajax view.
    def test_userlearningintention_progress_bar(self):
        View returns correct data for AJAX call

        pdb.set_trace()
        #Not logged in
        response = self.client.get('/interaction/learningintentiondetail'\
                                    '/1/progress/')
        self.assertEqual(response.status_code, 302)
        
        #Now logged in
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/interaction/learningintentiondetail/1/progress/', CONTENT_TYPE='application/json')
        self.assertEqual(response.status_code, 200)
        """

class UserAttachmentViewTests(TestCase):
    """Test view functions for user interaction with attachments"""
    
    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   'level': 'Basic',
                   'credits': 30,
                   }
    att1_data = {'code': 'DOC1',
                 'name': 'Reading List',
                 'desc': 'Useful stuff you might need',
                 'seq': 3,
                 'attachment': 'empty_attachment_test.txt',
                }
    att2_data = {'code': 'DOC2',
                 'name': 'Grammer Guide',
                 'desc': 'How do you even spell grammer?',
                 'seq': 2,
                 'attachment': 'empty_attachment_test.txt',
                }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()    
        self.course1 = Course(**self.course1_data)
        self.course1.save() 
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        self.lesson1 = Lesson(lesson_code="L1", 
                      lesson_name="Test Lesson 1",
                      course = self.course1)
        self.lesson1.save()
        #att1 attached to course
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att1.save()      
        #att2 attached to lesson
        self.att2 = Attachment(lesson=self.lesson1, **self.att1_data)
        self.att2.save()   
        
        
    def test_attachment_download(self):
        #Not logged in, redirect, dont record

        response = self.client.get('/interaction/attachment/2/download/')
        self.assertEqual(response.status_code, 302)
        self.assertRaises(ObjectDoesNotExist, UserAttachment.objects.get, id=2)
        
        #Now logged in
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/interaction/attachment/1/download/')
        self.assertEqual(response.status_code, 302)      
        u_att1 = UserAttachment.objects.get(pk=1)
        self.assertEqual(len(u_att1.hist2list()),1)
        response = self.client.get('/interaction/attachment/1/download/')
        u_att1 = UserAttachment.objects.get(pk=1)
        self.assertEqual(len(u_att1.hist2list()),2)
            
