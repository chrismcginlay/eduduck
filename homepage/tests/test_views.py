# Test the homepage views
from django.test import TestCase
from courses.forms import CourseNameForm
from courses.models import Course

class HomepageViewTests(TestCase):
    """Test the views of the homepage app"""
    
    fixtures = [
        'auth_user.json', 
        'courses.json'
    ]
        
    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'homepage/home.html')
        
    def test_homepage_is_found(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_uses_coursenameform(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['course_form'], CourseNameForm)
        
    def test_site_title(self):
        response = self.client.get('/')
        self.assertIn('<h1>EduDuck</h1>', response.content)
        
    def test_handle_no_courses_case(self):
        # Still renders template even if no courses
        
        Course.objects.all().delete()
        response = self.client.get('/')
        self.assertIn('<p>No courses?</p>', response.content)
    
    def test_handle_just_one_course(self):
        # Can render template if just one course
        
        ##leave just one course
        [c.delete() for c in Course.objects.all()[1:]]
        response = self.client.get('/')
        self.assertIn('div class="random_course pure-u-24-24"', 
                      response.content)
        
    def test_handle_two_courses(self):
        # Renders template with just two courses
        
        ##leave just two courses
        [c.delete() for c in Course.objects.all()[2:]]
        response = self.client.get('/')
        self.assertIn('div class="random_course pure-u-', 
                      response.content)
        
    def test_handle_three_courses(self):
        # Renders template with three courses
        
        ##three courses case
        [c.delete() for c in Course.objects.all()[3:]]
        response = self.client.get('/')
        self.assertIn('div class="random_course pure-u-', 
        response.content)   
       
    def test_account_profile_link_visible_when_logged_in(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/')
        self.assertIn('id="id_profile_link"', response.content)

    def test_account_avatar_visible_when_logged_in(self):
        self.client.login(username='chris', password='chris')
        response = self.client.get('/')
        self.assertIn('id="id_avatar"', response.content)

    def test_90_register_area_goes_away_when_logged_in(self):
        """ If a user is logged in, don't ask them to create an account """
        
        self.client.login(username='chris', password='chris')
        response = self.client.get('/')
        needle1 = 'id="id_social_auth_area">'
        self.assertNotIn(needle1, response.content)
        
        needle2 = '<div class="pure-u-1-2" id="id_account_status">'
        self.assertIn(needle2, response.content)
        
    def test_90_register_area_present_when_not_logged_in(self):
        response= self.client.get('/')
        needle1 = 'id="id_social_auth_area"'
        self.assertIn(needle1, response.content)
 
        needle2 = '<div class="pure-u-1-2" id="id_account_status">'
        self.assertNotIn(needle2, response.content)
        
    def test_course_create_area_present(self):
        response = self.client.get('/')
        needle = 'id="id_course_create"'
        self.assertIn(needle, response.content)

    def test_ssl_logo_area_present_in_footer(self):
        response = self.client.get('/')
        needle = 'id="id_ssl_logo"'
        self.assertIn(needle, response.content)        
