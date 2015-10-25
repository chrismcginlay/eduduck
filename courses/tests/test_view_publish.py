#courses/tests/test_view_publish.py
from django.http.response import (
    HttpResponseForbidden, 
    HttpResponseRedirect
)
from django.test import TestCase

class CourseViewPublishTests(TestCase):
    """Test courses.views.publish"""

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
        response = self.client.get('/courses/x/publish/')
        self.assertEqual(response.status_code, 404)

    def test_301_redirects_if_no_trailing_slash(self):
        response = self.client.get('/courses/1/publish')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url[-19:], '/courses/1/publish/')


    #
    # The not-logged-in situation
    #

    def test_not_logged_in_302_redirect(self):
        #redirect to login
        response = self.client.get('/courses/1/publish/')
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)
    
    #
    # The logged-in, not enrolled, not instructors/organisers situation
    #

    def test_logged_in_but_not_enrolled_or_author_403_permission_denied(self):
        self.client.login(username='gaby', password='gaby5')
        response = self.client.get('/courses/1/publish/')
        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(response.status_code, 403)


    #
    # The logged-in and enrolled as student situation
    #

    def test_logged_and_enrolled_but_not_author_403_permission_denied(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/courses/1/publish/')
        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(response.status_code, 403)


    #
    # The logged-in and is course author/instructor/organiser situation
    #

    def test_200_OK_get(self):
        self.client.login(username='helen', password='helen')
        response = self.client.get('/courses/7/publish/')
        self.assertEqual(response.status_code, 200)

    def test_200_OK_post(self):
        self.fail("write")

    def test_course_already_published_shows_appropriate_message(self):
        self.fail("write")
