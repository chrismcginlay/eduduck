"""
Unit tests for Interaction views
"""

import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from courses.models import Course
from lesson.models import Lesson
from outcome.models import LearningIntention, LearningIntentionDetail
from attachment.models import Attachment
from ..models import (UserCourse, 
                      UserLesson, 
                      UserLearningIntention,
                      UserLearningIntentionDetail,
                      UserAttachment)

course1_data = {'code': 'EDU02',
               'name': 'A Course of Leeches',
               'abstract': 'Learn practical benefits of leeches',
               }

course2_data = {'code': 'EDU03',
               'name': 'The Coarse and The Hoarse',
               'abstract': 'High volume swearing leading to loss of voice',
               }
course3_data = {'code': 'EDU04',
               'name': 'Pie Eating',
               'abstract': 'Gut Busting leads to Butt Gusting',
               }
course4_data = {'code': 'EDU05',
               'name': 'Golf',
               'abstract': 'The Contact Sport',
               }

class UserCourseViewTests(TestCase):
    """Test usercourse views"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.user4 = User.objects.create_user('James Maxwell', 'em@c', 'pdq')
        self.user4.is_active = True
        self.user4.save()

        self.course1 = Course(**course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save()
        self.course2 = Course(**course2_data)
        self.course2.instructor = self.user2
        self.course2.organiser = self.user2
        self.course2.save()
        self.course3 = Course(**course3_data)
        self.course3.instructor = self.user3
        self.course3.organiser = self.user3
        self.course3.save()
        self.course4 = Course(**course4_data)
        self.course4.instructor = self.user4
        self.course4.organiser = self.user4
        self.course4.save()

        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.uc2 = UserCourse(course=self.course2, user=self.user1)
        self.uc2.save()
        self.uc3 = UserCourse(course=self.course3, user=self.user1)
        self.uc3.save()

    def test_usercourse_single(self):
        """Test that the view contains the correct context vars"""

        u2 = self.user2.id
        c1 = self.course1.id
        url1 = "/interaction/user/{0}/course/{1}/".format(u2, c1)
        #Not logged in
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 302)

        #Now logged in
        self.client.login(username='Van Gogh', password='vancode')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['uc', 'history'])

        #non existent record
        response = self.client.get('/interaction/user/1/course/4000/')
        self.assertEqual(response.status_code, 404)


class UserLessonViewTests(TestCase):
    """Test userlesson views"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.user4 = User.objects.create_user('James Maxwell', 'em@c', 'pdq')
        self.user4.is_active = True
        self.user4.save()
        self.course1 = Course(**course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()
        self.course2 = Course(**course2_data)
        self.course2.organiser = self.user2
        self.course2.instructor = self.user2
        self.course2.save()     
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson1 = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson1.save()
        self.ul = UserLesson(user=self.user2, lesson=self.lesson1)
        self.ul.save()

    def test_userlesson_single(self):
        """View contains correct context variables"""

        u2 = self.user2.id
        l1 = self.lesson1.id
        url1 = "/interaction/user/{0}/lesson/{1}/".format(u2,l1)

        #Not logged in
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 302)

        #Now logged in
        self.client.login(username='Van Gogh', password='vancode')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['ul', 'history'])

        #non existent record
        response = self.client.get('/interaction/user/2/lesson/4000/')
        self.assertEqual(response.status_code, 404)

class UserLearningIntentionViewTests(TestCase):
    """Test views for learning intention interaction"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()    
        self.user2 = User.objects.create_user('Van Gogh', 'van@goch.com', 'vancode')
        self.user2.is_active = True
        self.user2.save()
        self.user3 = User.objects.create_user('Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.course1 = Course(**course1_data)
        self.course1.instructor = self.user2
        self.course1.organiser = self.user2
        self.course1.save() 

        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        self.lesson = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson.save() 
        self.li = LearningIntention(lesson=self.lesson, text="Intend...")
        self.li.save()
        self.uli = UserLearningIntention(user=self.user1, 
                                         learning_intention = self.li)
        self.lid1 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID A",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid2 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID B",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid3 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID C",
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

    def test_userlearningintention_cycle_redirect_not_enrolled(self):
        """If user not enrolled, can't cycle learning intentions"""

        not_enrolled_user = self.user3
        course = self.course1
        lid = self.lid1
        self.client.login(username='Chuck Norris', password='dontask')
        
        cycle_url = "/interaction/learningintentiondetail/{0}/cycle/" \
            .format(lid.pk)
        response = self.client.get(cycle_url)
        parsed_json = json.loads(response.content)
        self.assertEqual(parsed_json['authenticated'], True)
        self.assertEqual(parsed_json['enrolled'], False)
        self.assertEqual(parsed_json['course_pk'], 1)
   
    def test_userlearningintention_cycle_context(self):
        """Ensure correct context variables present for enrolled user"""

        enrolled_user = self.user1
        course = self.course1
        lid = self.lid1
        self.client.login(username="bertie", password="bertword")
        cycle_url = "/interaction/learningintentiondetail/{0}/cycle/" \
            .format(lid.pk)
        response = self.client.get(cycle_url)
        self.assertEqual(response.status_code, 200)
        parsed_json = json.loads(response.content)
        self.assertEqual(parsed_json['authenticated'], True)
        self.assertEqual(parsed_json['enrolled'], True)
        self.assertEqual(parsed_json['progress'], {u'SC': [0, 2], u'LO': [0, 1]})
        self.assertEqual(parsed_json['condition'], 1)
        

    def test_userlearningintention_progress_bar(self):
        """View returns correct data for AJAX call"""

        #self.fail("fix");
        #Not logged in
        response = self.client.get('/interaction/learningintentiondetail'\
                                    '/1/progress/')
        self.assertEqual(response.status_code, 302)

        #Now logged in
        self.client.login(username='bertie', password='bertword')
        #current implementation will not record progress without an 
        #initial cycle
        self.client.get('/interaction/learningintentiondetail/{0}/cycle/'\
            .format(self.lid1.pk))
        response = self.client.get(
            '/interaction/learningintentiondetail/{0}/progress/'\
            .format(self.lid1.pk))
        self.assertEqual(response.status_code, 200)


class UserLearningIntentionDetailViewTests(TestCase):
    """View functions for success criteria and learning outcomes"""

    fixtures = [
        'auth_user.json',
        'courses.json',
        'lessons.json',
        'outcome_lints.json',
        'interactions.json',
    ]

    def test_ajax_learningintentiondetail_status_requires_ajax(self):
        user = User.objects.get(pk=1) # chris in fixture
        self.client.login(username=user.username, password='chris')        
        lid1 = LearningIntentionDetail.objects.get(pk=1)
        lid2 = LearningIntentionDetail.objects.get(pk=2)
        lid3 = LearningIntentionDetail.objects.get(pk=3)
        # url1 - record of user interaction exists
        url1 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid1.pk)
        # url2 - record of user interaction exists
        url2 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid2.pk)
        # url3 - no previous user interaction with lid3
        url3 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid3.pk)
        self.client.login(username='chris', password='chris')
        
        response1 = self.client.get(url1, CONTENT_TYPE='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response1.status_code, 200, "Valid call 200")

        response1 = self.client.get(url1, CONTENT_TYPE='text/html')
        self.assertEqual(response1.status_code, 403, "Invalid call gives 403")

        response2 = self.client.get(url2, CONTENT_TYPE='application/json', 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response2.status_code, 200, "Valid call 200")

        response3 = self.client.get(url3, CONTENT_TYPE='application/json', 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response3.status_code, 200, "Valid call 200")

    def test_ajax_learningintentiondetail_status_correct(self):
        """Correctly return red, amber or green status"""
        user = User.objects.get(pk=1) # chris in fixture
        self.client.login(username=user.username, password='chris')        
        lid1 = LearningIntentionDetail.objects.get(pk=1)
        lid2 = LearningIntentionDetail.objects.get(pk=2)
        lid3 = LearningIntentionDetail.objects.get(pk=3) 
        lid4 = LearningIntentionDetail.objects.get(pk=4)
        # url1 - record of user interaction exists
        url1 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid1.pk)
        # url2 - record of user interaction exists
        url2 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid2.pk)
        # url3 - no previous user interaction with lid3
        url3 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid3.pk)
        # url4 - record of user interaction exists
        url4 = '/interaction/' \
            'learningintentiondetail/{0}/status/'.format(lid4.pk)
        self.client.login(username='chris', password='chris')
        
        response1 = self.client.get(url1, CONTENT_TYPE='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response2 = self.client.get(url2, CONTENT_TYPE='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response3 = self.client.get(url3, CONTENT_TYPE='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response4 = self.client.get(url4, CONTENT_TYPE='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
       
        self.assertEqual(response1.content, '{"status": "red"}', 
            "Correct status returned")
        self.assertEqual(response2.content, '{"status": "amber"}', 
            "Correct status returned")
        self.assertEqual(response3.content, '{"status": "red"}', 
            "Correct status returned")
        self.assertEqual(response4.content, '{"status": "green"}', 
            "Correct status returned")

class UserAttachmentViewTests(TestCase):
    """Test view functions for user interaction with attachments"""

    att1_data = {
        'name': 'Reading List',
        'desc': 'Useful stuff you might need',
        'seq': 3,
        'attachment': 'empty_attachment_test.txt',
    }
    att2_data = {
        'name': 'Grammer Guide',
        'desc': 'How do you even spell grammer?',
        'seq': 2,
        'attachment': 'empty_attachment_test.txt',
    }

    def setUp(self):
        self.user1 = User.objects.create_user(
            'bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()    
        self.user2 = User.objects.create_user('dave', 'dave@dave.com', 'dave')
        self.user2.is_active = True
        self.user2.save()

        self.user3 = User.objects.create_user(
            'Chuck Norris', 'chuck@tree.far', 'dontask')
        self.user3.is_active = True
        self.user3.save()
        self.course1 = Course(**course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save() 
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson1 = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson1.save()
        #att1 attached to course
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att1.save()      
        #att2 attached to lesson
        self.att2 = Attachment(lesson=self.lesson1, **self.att1_data)
        self.att2.save()   

    def test_attachment_download_not_logged_in(self):
        """Casual visitor - download not permitted, redirect to login"""
        a1 = self.att1.id
        a2 = self.att2.id
        url1 = '/interaction/attachment/{0}/download/'.format(a1)
        url1_r = '/accounts/login/?next={0}'.format(url1)
        url2 = '/interaction/attachment/{0}/download/'.format(a2)
        url2_r = '/accounts/login/?next={0}'.format(url2)

        #First try attachment linked to course page
        response = self.client.get(url1)
        self.assertRedirects(response, url1_r, 302, 200)
        self.assertRaises(ObjectDoesNotExist, UserAttachment.objects.get, id=a1)
        
        #Second, try attachment linked to a lesson page
        response = self.client.get(url2)
        self.assertRedirects(response, url2_r, 302, 200)
        self.assertRaises(ObjectDoesNotExist, UserAttachment.objects.get, id=a2)

    def test_attachment_download_author(self):
        """Course author can download attachments"""
        a1 = self.att1.id   #attached to course
        a2 = self.att2.id   #attached to lesson
        url1 = '/interaction/attachment/{0}/download/'.format(a1)
        url1_r = self.att1.get_absolute_url()
        url2 = '/interaction/attachment/{0}/download/'.format(a2)
        url2_r = self.att2.get_absolute_url()

        #First, try attachment linked to course page
        self.client.login(username='bertie', password='bertword')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 302)      
        #self.assertRedirects(response, url1_r, 302, 200)

        #Second, try attachment linked to lesson page
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 302)      
        #self.assertRedirects(response, url2_r, 302, 200)

    def test_attachment_download_loggedin_but_not_enrolled(self):
        """Not enrolled visitor - redirect to enrol page"""
        a1 = self.att1.id
        a2 = self.att2.id
        url1 = '/interaction/attachment/{0}/download/'.format(a1)
        url1_r = '/courses/{0}/enrol/'.format(self.att1.course.id)
        url2 = '/interaction/attachment/{0}/download/'.format(a2)
        url2_r = '/courses/{0}/enrol/'.format(self.att2.lesson.course.id)
        self.client.login(username='Chuck Norris', password='dontask')
        
        #First, try attachment linked to course page
        response = self.client.get(url1)
        self.assertRedirects(response, url1_r, 302, 200)      
        self.assertRaises(ObjectDoesNotExist, UserAttachment.objects.get, id=a1)

        #Second, try attachment linked to lesson page
        response = self.client.get(url2)
        self.assertRedirects(response, url2_r, 302, 200)
        self.assertRaises(ObjectDoesNotExist, UserAttachment.objects.get, id=a2)
 
    def test_attachment_download_loggedin_and_enrolled(self):
        """Enrolled visitor - download is recorded"""
        a1 = self.att1.id
        a2 = self.att2.id
        url1 = "/interaction/attachment/{0}/download/".format(a1)
        url2 = "/interaction/attachment/{0}/download/".format(a2)

        #First, try attachment linked to course page
        self.client.login(username='dave', password='dave')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 302)      
        u_att1 = UserAttachment.objects.get(
            user=self.user2.id,
            attachment=self.att1.id
        )
        self.assertEqual(len(u_att1.hist2list()),1)
        #Calling get(url1) again, history should grow by one log entry
        response = self.client.get(url1)
        u_att1 = UserAttachment.objects.get(
            user=self.user2.id,
            attachment=a1
        )
        self.assertEqual(len(u_att1.hist2list()),2)

        #Second, try attachment linked to lesson page
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 302)      
        u_att2 = UserAttachment.objects.get(
            user=self.user2.id,
            attachment=a2
        )
        self.assertEqual(len(u_att2.hist2list()),1)
        #Calling get(url2) again, history should grow by one log entry
        response = self.client.get(url2)
        u_att2 = UserAttachment.objects.get(
            user=self.user2.id,
            attachment=a2
        )
        self.assertEqual(len(u_att2.hist2list()),2)

