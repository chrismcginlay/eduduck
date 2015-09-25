#courses/tests/test_view_detail.py
from datetime import datetime
from decimal import Decimal
from time import mktime 
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.html import escape
from django.utils.timezone import utc

from courses.models import Course
from attachment.models import Attachment
from checkout.models import Payment
from interaction.models import (
    UserAttachment,
    UserLesson,
)
from lesson.models import Lesson
from checkout.models import PricedItem
from ..models import Course

class CourseViewdetailTests(TestCase):
    """Test courses.views.detail"""

    fixtures = [
        'auth_user.json',
        'checkout.json',
        'courses.json', 
        'lessons.json', 
        'outcome_lints.json', 
        'videos.json',
        'attachments.json',
        'interactions.json',
    ]
    
    #
    # Redirects and 404s etc.
    #
    
    def test_404_for_non_existent_course(self):    
        response = self.client.get('/courses/x/')
        self.assertEqual(response.status_code, 404)

    def test_301_redirects_if_no_trailing_slash(self):
        response = self.client.get('/courses/1')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url[-11:], '/courses/1/')

    def test_course_with_no_lessons_shows_appropriate_message(self):
        #See issue #87
        course5 = Course.objects.get(pk=5)
        course5.lesson_set.all().delete()
        organiser = course5.organiser.get_full_name()
        target = escape("{0} hasn\'t added any lessons yet!".format(organiser))
        response = self.client.get('/courses/5/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(target, response.content)


    #
    # The not-logged-in situation
    #

    def test_200_not_logged_in(self):
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template_not_logged_in(self):
        response = self.client.get('/courses/1/') 
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_context_not_logged_in(self):
        response = self.client.get('/courses/1/')
        self.assertIn('course', response.context)
        self.assertIn('attachments', response.context)
        self.assertIsNone(response.context['uc'])
        self.assertIsNone(response.context['history'])
        self.assertIsNone(response.context['lessons'])
        self.assertEqual('noauth', response.context['status'])
        self.assertEqual(response.context['course'].pk, 1)
        self.assertFalse(response.context['user_can_edit'])
        self.assertIn('fee_value', response.context)

    def test_course_view_200_despite_no_PricedItem(self):
        """Non-existence of priced item for course is OK"""
        course1 = Course.objects.get(pk=1)
        priced_item = PricedItem.objects.get(
            content_type_id=13, object_id=course1.pk)
        #deleting priced_item should trigger a new priced_item in detail view
        priced_item.delete()
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['fee_value'], Decimal(1.00))

    def test_no_enrol_buttons_yes_signup_button_if_not_loggedin(self):
        response = self.client.get('/courses/1/')
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_button2', response.content)
        resp = response.content.replace("\n", "").replace("\t", "")
        self.assertIn('id_signup_button', resp)
         
    def test_organiser_instructor_links_working_when_not_logged_in(self):
        response = self.client.get('/courses/1/')
        organiser = response.context['course'].organiser
        instructor = response.context['course'].instructor
        t = '<p>Course organiser <a href="/accounts/profile/{1}/public/">{0}</a>'
        target = t.format(organiser.get_full_name(), organiser.pk)
        resp = response.content.replace("\n", "").replace("\t", "")
        self.assertIn(target, resp)
        
        t = '<p>Course instructor <a href="/accounts/profile/{1}/public/">{0}</a>'
        target = t.format(instructor.get_full_name(), instructor.pk)
        self.assertIn(target, resp)
    
    #
    # The logged-in but not enrolled situation for non-instructors/organisers
    #

    def test_200_logged_in_not_yet_enrolled(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template_not_yet_enrolled(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/') 
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_context_logged_in_not_enrolled(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/')
        self.assertEqual(response.context['course'].pk, 1)
        self.assertEqual(response.context['status'], 'auth_not_enrolled')
        self.assertIn('attachments', response.context)
        self.assertIsNone(response.context['uc'])
        self.assertIsNone(response.context['history'])
        self.assertIsNone(response.context['lessons'])
        self.assertFalse(response.context['user_can_edit'])
        self.assertIn('fee_value', response.context)
        self.assertIn('fee_value_cents', response.context)
        self.assertIn('currency', response.context)

    def test_context_attachment_got_something(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/')
        expected_list_of_tuples = [
            (None, Attachment.objects.get(pk=1)),
            (None, Attachment.objects.get(pk=2)),
            (None, Attachment.objects.get(pk=3)),
        ]
        self.assertEqual(
            expected_list_of_tuples, response.context['attachments'])

    def test_enrol_buttons_logged_in_not_enrolled_not_instructor(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/')
        self.assertIn('id_enrol_area', response.content)
        self.assertIn('id_enrol_button', response.content)
        self.assertIn('id_enrol_button2', response.content)

    def test_enrol_button_if_not_enrolled_shows_course_fee(self):
        self.client.login(username='gaby', password='gaby5')
        course1 = Course.objects.get(pk=1)
        priced_item = PricedItem.objects.get(object_id=course1.id)   
        response = self.client.get('/courses/1/')
        self.assertEqual(response.context['fee_value'], priced_item.fee_value)
        self.assertRegexpMatches(
            response.content,
            "<button id=\\\'id_enrol_button\\\'[\s\S]*Enrol &#163;{0}"\
            "[\S\s]*</button>".format(priced_item.fee_value))
        self.assertRegexpMatches(
            response.content,
            "<button id=\\\'id_enrol_button2\\\'[\s\S]*Enrol &#163;{0}"\
            "[\S\s]*</button>".format(priced_item.fee_value))
    
    def test_stripe_Pay_with_Card_visible_if_not_enrolled(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/')
        self.assertRegexpMatches(
            response.content, 
            "<script[\S\s]*src=\"https://checkout.stripe.com/checkout.js\""\
            " class=\"stripe-button\"")

    def test_cannot_access_lesson_2_when_not_enrolled(self):
        self.client.login(username='helmi', password='plate509')
        response = self.client.get('/courses/3/lesson/2/')
        self.assertEqual(response.status_code, 302)

    def test_POST_course_enrol_200(self):
        """POSTing form course_enrol reloads page with 200 OK"""
        #create payment record for gaby on course 1
        #payment ultimately should obtain its information from a PricedItem
        course1 = Course.objects.get(pk=1)
        user = User.objects.get(pk=3)   #Gaby
        priced_item = PricedItem.objects.get(object_id=course1.id)   
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=course1,
            fee_value=priced_item.fee_value,
            datestamp=current_time,
        )
        payment.save()

        self.client.login(username='gaby', password='gaby5')
        form_data = {'course_enrol':'Enrol'}
        response = self.client.post('/courses/1/', form_data)
        self.assertEqual(response.status_code, 200)

    def test_POST_course_enrol_correct_template(self):
        """POSTing form course_enrol reloads page with correct template"""
        #create payment record for gaby on course 1
        #payment ultimately should obtain its information from a PricedItem
        course1 = Course.objects.get(pk=1)
        user = User.objects.get(pk=3)   #Gaby
        priced_item = PricedItem.objects.get(object_id=course1.id)   
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=course1,
            fee_value=priced_item.fee_value,
            datestamp=current_time,
        )
        payment.save()

        self.client.login(username='gaby', password='gaby5')
        form_data = {'course_enrol':'Enrol'}
        response = self.client.post('/courses/1/', form_data)
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_POST_course_enrol_context_has_paid(self):
        """POSTing form course_enrol reloads with proper context variables"""
        
        #create payment record for gaby on course 1
        #payment ultimately should obtain its information from a PricedItem
        course1 = Course.objects.get(pk=1)
        user = User.objects.get(pk=3)   #Gaby
        priced_item = PricedItem.objects.get(object_id=course1.id)   
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=course1,
            fee_value=priced_item.fee_value,
            datestamp=current_time,
        )
        payment.save()

        #presence of payment record should permit enrolment
        self.client.login(username='gaby', password='gaby5')
        form_data = {'course_enrol':'Enrol'}
        response = self.client.post('/courses/1/', form_data)
        self.assertIn('uc', response.context)
        self.assertIsNotNone(response.context['lessons'])
        self.assertIsNotNone(response.context['history'])
        self.assertEqual(response.context['course'].pk, 1)
        self.assertEqual(response.context['status'], 'auth_enrolled')
        self.assertFalse(response.context['user_can_edit'])
        self.assertEqual(response.context['uc'].active, True)        
        self.assertEqual(response.context['uc'].withdrawn, False)        
        self.assertEqual(response.context['uc'].completed, False)        
    
    def test_POST_course_enrol_no_enrol_buttons(self):
        #create payment record for gaby on course 1
        #payment ultimately should obtain its information from a PricedItem
        course1 = Course.objects.get(pk=1)
        user = User.objects.get(pk=3)   #Gaby
        priced_item = PricedItem.objects.get(object_id=course1.id)   
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=course1,
            fee_value=priced_item.fee_value,
            datestamp=current_time,
        ).save()

        self.client.login(username='gaby', password='gaby5')
        form_data = {'course_enrol':'Enrol'}
        response = self.client.post('/courses/1/', form_data)
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_button2', response.content)

    #
    # The logged-in and enrolled situation
    #

    def test_200_enrolled(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template_enrolled(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/') 
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    def test_context_enrolled(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        self.assertEqual(response.context['course'].pk, 3)
        self.assertEqual(response.context['status'], 'auth_enrolled')
        self.assertIn('attachments', response.context)
        self.assertIsNotNone(response.context['uc'])
        self.assertIsNotNone(response.context['history'])
        self.assertIsNotNone(response.context['lessons'])
        self.assertFalse(response.context['user_can_edit'])

    def test_context_enrolled_lesson_list(self):
        """Tuple (lessons, visited_flag) in lesson context variable"""
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        expected_list_of_tuples = [
            (Lesson.objects.get(pk=11), UserLesson.objects.get(pk=1)),
            (Lesson.objects.get(pk=12), UserLesson.objects.get(pk=2)),
            (Lesson.objects.get(pk=13), None),
            (Lesson.objects.get(pk=14), None),
        ]
        self.assertEqual(expected_list_of_tuples, response.context['lessons'])

    def test_context_enrolled_attachment_list(self):
        """Tuple (user_attachment|None, attachment) in context variable"""
        self.client.login(username='chris', password='chris')
        self.client.get('/interaction/attachment/1/download/')
        self.client.get('/interaction/attachment/3/download/')
        response = self.client.get('/courses/1/')
        expected_list_of_tuples = [
            (UserAttachment.objects.get(pk=1), Attachment.objects.get(pk=1)),
            (None, Attachment.objects.get(pk=2)),
            (UserAttachment.objects.get(pk=2), Attachment.objects.get(pk=3)),
        ]
        self.assertEqual(
            expected_list_of_tuples, response.context['attachments'])

    def test_uc_context_keys_for_activity(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        self.assertEqual(response.context['uc'].active, True)
        self.assertEqual(response.context['uc'].withdrawn, False)
        self.assertEqual(response.context['uc'].completed, False)

    def test_no_enrol_buttons_when_enrolled(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_button2', response.content)

    def test_enrolled_message_when_enrolled(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/3/')
        self.assertIn('You\'re enrolled on this course', response.content)

    def test_can_access_lesson_2_when_enrolled(self):
        course = Course.objects.get(pk=3)
        user = User.objects.get(pk=1)
        lesson2 = course.lesson_set.first().get_next()
        self.client.login(username='chris', password='chris')
        priced_item = PricedItem.objects.get(object_id=course.id)   
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=course,
            fee_value=priced_item.fee_value,
            datestamp=current_time,
        ).save()
        response = self.client.get(lesson2.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_POST_withdraw_when_enrolled(self):
        self.client.login(username='chris', password='chris')
        form_data = {'course_withdraw':'Withdraw'} 
        response = self.client.post('/courses/3/', form_data)
        self.assertIn('<p>Current status: withdrawn</p>', response.content)
        self.assertIn(
            '<input type="submit" name="course_reopen"', response.content)
        self.assertEqual(response.context['uc'].active, False)        
        self.assertEqual(response.context['uc'].withdrawn, True)        
        self.assertEqual(response.context['uc'].completed, False)        
        self.assertEqual(response.context['status'], 'auth_enrolled')

    def test_POST_reopen_when_withdrawn(self):
        self.client.login(username='chris', password='chris')
        form_data = {'course_withdraw':'Withdraw'} 
        response = self.client.post('/courses/3/', form_data)
        form_data = {'course_reopen':'Re-open'} 
        response = self.client.post('/courses/3/', form_data)
        self.assertEqual(response.context['uc'].active, True)        
        self.assertEqual(response.context['uc'].withdrawn, False)        
        self.assertEqual(response.context['uc'].completed, False)        
        self.assertEqual(response.context['status'], 'auth_enrolled')

    def test_POST_complete_when_enrolled(self):
        self.client.login(username='chris', password='chris')
        form_data = {'course_complete':'Complete'} 
        response = self.client.post('/courses/3/', form_data)
        self.assertIn('<p>Current status: completed</p>', response.content)
        self.assertIn(
            '<input type="submit" name="course_reopen"', response.content)
        self.assertEqual(response.context['uc'].active, False)        
        self.assertEqual(response.context['uc'].withdrawn, False)
        self.assertEqual(response.context['uc'].completed, True)        
        self.assertEqual(response.context['status'], 'auth_enrolled')

    #
    # The logged-in but can't enroll situation 'cos instructor/organiser 
    #
    
    def test_200_logged_in_cant_enrol(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/3/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template_logged_in_cant_enrol(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/3/') 
        self.assertTemplateUsed(response, 'courses/course_detail.html')
    
    def test_context_logged_in_cant_enrol(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/3/') 
        self.assertEqual(response.context['status'], 'auth_bar_enrol')
        self.assertTrue(response.context['user_can_edit'])
        self.assertIn('attachments', response.context)
        self.assertIsNone(response.context['uc'])
        self.assertIsNone(response.context['history'])
        self.assertIsNone(response.context['lessons'])
        self.assertIn('attachments', response.context)
        self.assertIn(
            'You are involved in running this course', response.content)

    def test_no_enrol_buttons_when_cant_enrol(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/')
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_button2', response.content)

