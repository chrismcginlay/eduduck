# Test the homepage views
from django.test import TestCase
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
        
    def test_site_title(self):
        response = self.client.get('/')
        self.assertInHTML('<h1>EduDuck</h1>', response.content)
        
    def test_handle_no_courses_case(self):
        # Still renders template even if no courses
        
        import pdb; pdb.set_trace()
        Course.objects.all().delete()
        response = self.client.get('/')
        self.assertInHTML('<p>No courses?</p>', response.content)
        