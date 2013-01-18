"""
Unit tests for Courses app
"""

from django.test import TestCase
from courses.models import Course

class CourseModelTests(TestCase):
    """Test the model used to represent courses"""

#TODO load data from JSON fixtures if these instances become irksome
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': 5,
                   'course_credits': -20,
                   }                 
    
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        
    def test_course_create(self):
        """All instance attributes are created OK"""
        for key,val in self.course1_data.items():
            self.assertEqual(self.course1.__dict__[key], val)

class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    course2_data = {'course_code': 'FBR9',
                   'course_name': 'Basic Knitting',
                   'course_abstract': 'Casting on',
                   'course_organiser': 'Lee Marvin',
                   'course_level': 5,
                   'course_credits': -20,
                   }  
                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()    

    def test_course_index(self):
        """Check course index page loads OK and has correct variables"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        for x in ['course_list', 'course_count']:
            self.assertTrue(x in response.context)
            
    def test_course_single(self):
        """Check individual course page loads"""
        response = self.client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)
        #check template variables present and correct
        self.assertTrue('course' in response.context)
        self.assertEqual(response.context['course'].pk, 1)
        
        #check 404 for non-existent course
        response = self.client.get('/courses/5/')
        self.assertEqual(response.status_code, 404)
        
        #check redirect for trailing slash
        response = self.client.get('/courses/5')
        self.assertEqual(response.status_code, 301)
        
        
        
        