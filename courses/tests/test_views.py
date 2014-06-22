# Unit tests for courses views

import json
from datetime import datetime
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden
from django.test import TestCase
from django.utils.html import escape

from bio.models import Bio

from interaction.models import UserCourse
from lesson.models import Lesson
from ..forms import (
    NAME_FIELD_REQUIRED_ERROR,
    ABSTRACT_FIELD_REQUIRED_ERROR,
    )
from ..models import Course
from ..views import CourseFullForm

class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {
        'code': 'EDU02',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
    }
    course2_data = {
        'code': 'FBR9',
        'name': 'Basic Knitting',
        'abstract': 'Casting on',
    }  
    course3_data = {
        'code': 'G3',
        'name': 'Nut Bagging',
        'abstract': 'Put the nuts in the bag',
    }
    lesson1_data = {
        'code': 'B1',
        'name': 'Introduction to Music',
        'abstract': 'A summary of what we cover',
    }
    lesson2_data = {
        'code': 'B2',
        'name': 'Stuff',
        'abstract': 'Not a lot',
    }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('hank', 'hank@example.com', 'hankdo')
        self.user2.is_active = True
        self.user2.save()

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
        
    def test_course_page_has_edit_button_for_organiser_instructor(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/')
        self.assertIn("id='id_edit_course'", response.content)
        self.assertEqual(response.context['user_can_edit'], True)

    def test_course_page_has_no_edit_button_if_not_organiser_instructor(self):
        self.client.login(username='hank', password='hankdo')
        response = self.client.get('/courses/1/')
        self.assertNotIn("id='id_edit_course'", response.content)
        self.assertEqual(response.context['user_can_edit'], False)

    def test_course_edits_actually_saved(self):
        self.client.login(username='bertie', password='bertword')
        mod_data = {'code': 'F1', 'name': 'Dingbat', 'abstract': 'Fingbot',
                    'organiser': self.user1, 'instructor': self.user1,}
        ##This should trigger modification of the course
        response = self.client.post('/courses/1/edit/', mod_data)
        
        ##Then visiting the course should reflect the changes
        response = self.client.get('/courses/1/')
        self.assertContains(response, 
            '<h3>F1 : Dingbat Course Homepage</h3>', html=True)
        self.assertIn('<p>Fingbot</p>', response.content)
        
    def test_course_edit_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/1/edit/')  
        login_redirect_url = '/accounts/login/?next=/courses/1/edit/'
        self.assertRedirects(response, login_redirect_url, 302, 200)

    def test_course_edit_forbidden_if_user_not_permitted(self):
        self.client.login(username='hank', password='hankdo')
        response = self.client.get('/courses/1/edit/')
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_course_edit_200_if_user_permitted(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/') 
        self.assertEqual(response.status_code, 200)
    
    def test_course_edit_uses_correct_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/') 
        self.assertTemplateUsed(response, 'courses/course_edit.html')
        
    def test_course_edit_page_uses_correct_form(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIsInstance(response.context['form'], CourseFullForm)
        
    def test_course_edit_page_has_correct_data_prefilled(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIn('value="EDU02"', response.content)
        self.assertIn('value="A Course of Leeches"',
                      response.content)
        self.assertIn(
            'Learn practical benefits of leeches</textarea>', 
            response.content)
        
    def test_course_edit_page_validation_errors_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/1/edit/', data={
            'code': '',
            'name': '',
            'abstract': ''
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_edit.html')
        
    def test_course_create_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/create/')
        login_redirect_url = '/accounts/login/?next=/courses/create/'
        self.assertRedirects(response, login_redirect_url, 302, 200)
        
    def test_course_create_page_200_if_loggedin(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertEqual(response.status_code, 200)
  
    def test_course_create_view_uses_correct_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertTemplateUsed(response, 'courses/course_create.html')
        
    def test_course_create_view_uses_correct_form(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertIsInstance(response.context['form'], CourseFullForm)
        
    def test_course_create_page_has_correct_title_and_breadcrumb(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        needle = "<h2 id='id_page_title'>Create a Course</h2>"
        self.assertIn("<p id='id_breadcrumb'>", response.content)
        self.assertIn(needle, response.content)
        
    def test_course_create_page_has_correct_fields(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertIn('<input id="id_code"', response.content)
        self.assertIn('<input id="id_name"', response.content)
        self.assertIn('id="id_abstract"', response.content)

    def test_course_create_page_has_create_button(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        target = 'id="id_course_create"'
        self.assertIn(target, response.content)
        
    def test_course_create_page_invalid_form_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_create.html')
            
    def test_course_create_page_validation_errors_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': '',
        })
        expected_errors = (
            NAME_FIELD_REQUIRED_ERROR,
            ABSTRACT_FIELD_REQUIRED_ERROR,
        )
        for err in expected_errors:
            self.assertContains(response, err)

    def test_course_create_page_doesnot_show_errors_by_default(self):
        """ Check that errors don't show up when the form first loads """
        
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        not_expected_errors = (
            NAME_FIELD_REQUIRED_ERROR,
            ABSTRACT_FIELD_REQUIRED_ERROR,
            )
        for err in not_expected_errors:
            self.assertNotContains(response, err)
            
        
    def test_course_create_page_invalid_form_passes_form_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': ''
        })
        self.assertIsInstance(response.context['form'], CourseFullForm)
    
    def test_course_index_not_logged_in(self):
        """Check course index page loads OK and has correct variables"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        self.assertTrue(x in response.context for x in ['course_list', 
                                                        'course_count'])

    def test_course_index_logged_in(self):
        """Check course index loads for logged in user"""

        url1 = '/courses/'
        self.client.login(username='bertie', password='bertword')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('course_list', response.context, \
            "Missing template var: course_list")
        self.assertIn('course_count', response.context, \
            "Missing template var: course_count")
        
        
    def test_course_single_auth(self):
        """Check course page loads for authorised user"""

        c1 = self.course1.pk
        url1 = '/courses/{0}/'.format(c1)
        c2 = self.course2.pk
        url2 = '/courses/{0}/'.format(c2)

        #First, when the user is not registered on course
        self.client.login(username='bertie', password='bertword')
        response = self.client.get(url1)
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
        response = self.client.get(url1)
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
        self.assertEqual(response.context['course'].pk, c1)
        
        #check 404 for non-existent course
        response = self.client.get('/courses/x/')
        self.assertEqual(response.status_code, 404)
        
        #check redirect for trailing slash
        response = self.client.get('/courses/1')
        self.assertEqual(response.status_code, 301)

        #see that unregistered user get the register button
        response = self.client.get(url2)
        self.assertIn('course_register', response.content)
        self.assertEqual(response.context['status'], 'auth_noreg')
        
        #see that registration button works (user registers)
        response = self.client.post(url2, {'course_register':'Register'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertEqual(response.context['course'], self.course2)
        self.assertIn('course_complete', response.content)
        self.assertIn('course_withdraw', response.content)
        self.assertEqual(response.context['uc'].active, True)        
        
        #see that a registered user can withdraw
        response = self.client.post(url2, {'course_withdraw':'Withdraw'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_reopen', response.content)
        self.assertEqual(response.context['uc'].active, False)        
        self.assertEqual(response.context['uc'].withdrawn, True)        
        
        #see that a withdrawn user can reopen
        response = self.client.post(url2, {'course_reopen':'Re-open'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_complete', response.content)
        self.assertIn('course_withdraw', response.content)
        self.assertEqual(response.context['uc'].active, True)
        self.assertEqual(response.context['uc'].withdrawn, False)                
        
        #see that a registered user can complete
        response = self.client.post(url2, {'course_complete':'Complete'})
        self.assertEqual(response.context['status'], 'auth_reg')
        self.assertIn('course_reopen', response.content)
        self.assertEqual(response.context['uc'].active, False)                
        self.assertEqual(response.context['uc'].completed, True)        
        
        
    def test_course_single_unauth(self):        
        """Check individual course page loads for unauth user"""

        c1 = self.course1.pk
        url1 = '/courses/{0}/'.format(c1)
        response = self.client.get(url1)
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
        self.assertEqual(response.context['course'].pk, c1)   
        

    def test_86_organiser_instructor_name(self):
        """Course templates show either full name or username of 
instructor"""

        # Load up the course index page
        c2 = self.course2
        url1 = '/courses/'
        c2.instructor.first_name="Hank"
        c2.instructor.last_name="Rancho"
        c2.instructor.save()
        response = self.client.get(url1)
        
        # Check username appears for organiser
        org = c2.organiser
        t = '<p>Course organiser <a href="/accounts/bio/public/{1}/">{0}</a>'
        target = t.format(org.username, org.pk)
        resp = response.content.replace("\n", "").replace("\t", "")
        self.assertIn(target, resp)
        
        # Check full name appears for instructor
        inst = c2.instructor
        t = '<p>Course instructor <a href="/accounts/bio/public/{1}/">{0}</a>'
        target = t.format(inst.get_full_name(), inst.pk)
        self.assertIn(target, resp)
        
        # Load up a course single page
        c2 = self.course2
        url2 = '/courses/{0}/'.format(c2.pk)
        c2.instructor.first_name="Hank"
        c2.instructor.last_name="Rancho"
        c2.instructor.save()
        response = self.client.get(url2)

        # Check username appears for organiser
        org = c2.organiser
        t = '<p>Course organiser <a href="/accounts/bio/public/{1}/">{0}</a>'
        target = t.format(org.username, org.pk)
        resp = response.content.replace("\n", "").replace("\t", "")
        self.assertIn(target, resp)
        
        # Check full name appears for instructor
        inst = c2.instructor
        t = '<p>Course instructor <a href="/accounts/bio/public/{1}/">{0}</a>'
        target = t.format(inst.get_full_name(), inst.pk)
        self.assertIn(target, resp)
        
    def test_87_course_with_no_lessons_shows_template_error(self):
        """Should show 'course organiser hasn't added any lessons yet"""

        # Load up a course 2 single page (has no lessons)
        c2 = self.course2
        url2 = '/courses/{0}/'.format(c2.pk)
        c2.organiser.first_name="Bertrand"
        c2.organiser.last_name="Bouffant"
        c2.organiser.save()
        response = self.client.get(url2)
        resp = response.content.replace("\n", "").replace("\t", "")

        # See organiser named properly in message
        organiser = c2.organiser.get_full_name()
        t = escape("{0} hasn't added any lessons yet!".format(organiser))
        self.assertIn(t, resp)
               
    def test_90_not_logged_in_shows_sign_up_button_and_form(self):
        """ If not logged in, invite to sign up """
        
        c1 = self.course1
        response = self.client.get(c1.get_absolute_url())
        self.assertIn('id_signup_button', response.content)
        self.assertIn('id_signup_area', response.content)
        
    def test_90_logged_in_but_not_enrolled(self):
        """ User not enrolled, invite to enrol x2 areas """
        
        self.client.login(username='bertie', password='bertword')
        c1 = self.course1
        response = self.client.get(c1.get_absolute_url())
        self.assertIn('id_enrol_button', response.content)
        self.assertIn('id_enrol_area', response.content)
        
    def test_90_logged_in_and_enrolled(self):
        """ User is enrolled, hide both enrol areas """

        self.client.login(username='bertie', password='bertword')
        uc = UserCourse(user=self.user1, course=self.course1)
        uc.save()
        c1 = self.course1
        response = self.client.get(c1.get_absolute_url())
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_area', response.content)