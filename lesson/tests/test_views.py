# Unit tests for lesson views

from datetime import datetime
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden
from django.test import TestCase

from lesson.models import Lesson
from interaction.models import UserCourse

class LessonViewTests(TestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        ]
    
    def test_lesson_unauth(self):
        """Test view of single lesson for unauthenticated user"""
        
        l1 = Lesson.objects.get(pk=1)
        url1 = '/courses/{0}/lesson/{1}/'.format(l1.course.pk,l1.pk)
        
        self.client.logout()
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
                        for x in ['course', 'lesson', 'ul', 'attachments',
                        'history', 'learning_intentions'])
        self.assertEqual(response.context['history'], None, 
                        "There should be no history - unauthenticated")
        self.assertEqual(response.context['ul'], None, 
                        "There should be no userlesson - unauthenticated")                 
        self.assertNotIn('id_lesson_edit', response.content,
                        "There should be no edit button -unauthenticated")

    def test_lesson_loggedin_and_enrolled_on_course(self):

        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        l1 = Lesson.objects.get(pk=1)
        url1 = '/courses/{0}/lesson/{1}/'.format(l1.course.pk, l1.pk)

        # Enrol the user on the course
        uc = UserCourse(user=user, course=l1.course)
        uc.save()
        # Visit the page
        response = self.client.get(url1)
        
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
        response = self.client.post(url1, {'lesson_complete':'Complete'})
        self.assertIn('lesson_reopen', response.content)
        self.assertEqual(response.context['ul'].completed, True) 
        
        #see that lesson reopen button works 
        response = self.client.post(url1, {'lesson_reopen':'Re-open'})
        self.assertIn('lesson_complete', response.content)
        self.assertEqual(response.context['ul'].completed, False)        

    def test_lesson_loggedin_and_but_not_enrolled_on_course(self):

        l1 = Lesson.objects.get(pk=1)
        url1 = '/courses/{0}/lesson/{1}/'.format(l1.course.pk, l1.pk)
        l2 = Lesson.objects.get(pk=8)
        url2 = '/courses/{0}/lesson/{1}/'.format(l2.course.pk, l2.pk)

        response = self.client.get(url2)
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - unregistered")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - unregistered")  

    def test_lesson_page_has_edit_button_for_organiser_instructor(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/1/lesson/1/')
        self.assertIn("id='id_edit_lesson'", response.content)
        self.assertEqual(response.context['user_can_edit_lesson'], True)

    def test_lesson_page_has_no_edit_button_if_not_organiser_instructor(self):
        self.client.login(username='helmi', password='plate509')
        response = self.client.get('/courses/1/lesson/1/')
        self.assertNotIn("id='id_edit_course'", response.content)
        self.assertEqual(response.context['user_can_edit_lesson'], False)

    def test_lesson_edits_actually_saved(self):
        self.fail("write me")

    def test_lesson_edit_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/1/lesson/1/edit/')  
        login_redirect_url = '/accounts/login/?next=/courses/1/lesson/1/edit/'
        self.assertRedirects(response, login_redirect_url, 302, 200)

    def test_lesson_edit_forbidden_if_user_not_permitted(self):
        self.client.login(username='helmi', password='plate509')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_lesson_edit_200_if_user_permitted(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/1/lesson/1/edit/') 
        self.assertEqual(response.status_code, 200)

    def test_lesson_edit_page_has_correct_title_and_breadcrumb(self):
        self.fail("write me")
    def test_lesson_edit_uses_correct_template(self):
        self.fail("write me")
    def test_lesson_edit_page_uses_correct_form(self):
        self.fail("write me")
    def test_lesson_edit_page_uses_correct_formsets(self):
        self.fail("write me")
    def test_lesson_edit_page_validation_errors_sent_to_template(self):
        self.fail("write me")
    def test_lesson_edit_page_validation_errors_generate_error_msg(self):
        self.fail("write me")
    def test_lesson_edit_page_has_lesson_abstract_area(self):
        self.fail("write me")
    def test_lesson_edit_page_has_populated_lesson_area(self):
        self.fail("write me")
    def test_lesson_edit_page_has_video_area(self):
        self.fail("write me")

