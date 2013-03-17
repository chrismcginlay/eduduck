from django.test import TestCase
from courses.models import Course, Lesson
from ..models import (LearningIntention,
                      SuccessCriterion,
                      LearningOutcome)
import pdb

class OutcomeViewTests(TestCase):
    """Test the outcome specific views"""
    
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 'Basic',
                   'course_credits': 30,
                   }
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
                   
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()        
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    li_text = "Practise")
        self.learningintention1.save()                                            
        self.successcriterion1 = SuccessCriterion(
            learning_intention = self.learningintention1, 
            criterion_text = "Choose Topaz"
        )
        self.successcriterion1.save()                                          
        self.learningoutcome1 = LearningOutcome(
            learning_intention = self.learningintention1, 
            lo_text = "Calculate 6*9"
        )
        self.learningoutcome1.save()    
    
    def test_learning_intention(self):
        """Test view of a single learning intention"""
        
        response = self.client.get('/lesson/1/lint/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['lesson_id', 'lesson_intention_id'])
        self.assertIn("Choose Topaz", response.content, "LO missing")
        self.assertIn("Calculate 6*9", response.content, "SC missing")

        #test non-existing LI        
        response = self.client.get('/lesson/1/lint/5/')
        self.assertEqual(response.status_code, 404)