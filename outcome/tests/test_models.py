from django.test import TestCase

from courses.models import Course, Lesson
from ..models import (LearningIntention,
                     SuccessCriterion,
                     LearningOutcome)

import pdb 

class OutcomeModelTests(TestCase):
    """Test the models of the outcome app"""

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
            criterion_text = "Choose"
        )
        self.successcriterion1.save()                                          
        self.learningoutcome1 = LearningOutcome(
            learning_intention = self.learningintention1, 
            lo_text = "Calculate"
        )
        self.learningoutcome1.save()    
                     
    def test_learningIntention_create(self):
        """LearningIntention instance attributes are created OK"""
        
        self.assertEqual(self.learningintention1.lesson, self.lesson1)
        self.assertEqual(self.learningintention1.li_text, "Practise")
    
    def test_successCriterion_create(self):
        """SuccessCriterion instance attributes are created OK"""
        self.assertEqual(self.successcriterion1.learning_intention, self.learningintention1)
        self.assertEqual(self.successcriterion1.criterion_text, "Choose")
        
    def test_learningOutcome_create(self):
        """LearningOutcome instance attributes are created OK"""
        self.assertEqual(self.learningoutcome1.learning_intention, self.learningintention1)
        self.assertEqual(self.learningoutcome1.lo_text, "Calculate")