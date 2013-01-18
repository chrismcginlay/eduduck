"""
Unit tests for Courses app
"""

from django.test import TestCase
from courses.models import Course, Lesson, Video, Attachment

class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

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
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    video1_data = {'video_code': 'MV2',
                   'url': 'http://youtu.be/LIM--jfnKeU',
                   'video_name': 'Music introduction',
                  }
    attachment1_data = {'att_code': 'DOC1',
                        'att_name': 'Reading List',
                        'att_desc': 'Useful stuff you might need',
                        'att_seq': 3,
                        }
    
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.course2 = Course(**self.course2_data)
        self.course2.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.video1 = Video(course=self.course1, **self.video1_data)
        self.video1.save()
        self.video2 = Video(lesson=self.lesson1, **self.video1_data)
        self.video2.save()
        self.attachment1 = Attachment(course=self.course1, 
                                      **self.attachment1_data)
        self.attachment1.save()
        
    def test_course_create(self):
        """All instance attributes are created OK"""
        for key,val in self.course1_data.items():
            self.assertEqual(self.course1.__dict__[key], val)
    
    def test_lesson_create(self):
        for key,val in self.lesson1_data.items():
            self.assertEqual(self.lesson1.__dict__[key], val)
        self.assertEqual(self.lesson1.course, self.course1)
            
    def test_video_create(self):
        #Associated with course
        for key,val in self.video1_data.items():
            self.assertEqual(self.video1.__dict__[key], val)
        self.assertEqual(self.video1.course, self.course1)
            
        #Associated with lesson
        for key,val in self.video1_data.items():
            self.assertEqual(self.video2.__dict__[key], val)
        self.assertEqual(self.video2.lesson, self.lesson1)
            
    def test_attachment_create(self):
        for key,val in self.attachment1_data.items():
            self.assertEqual(self.attachment1.__dict__[key], val)   
        self.assertEqual(self.attachment1.course, self.course1)

    def test_userProfile_create(self):
        assert (False)  #stub
    
    def test_userProfile_Lesson_create(self):
        assert (False)  #stub
    
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
        
        
        
        