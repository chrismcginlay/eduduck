from django.test import TestCase

from courses.models import Course, Lesson
from ..models import LearningIntention, LearningIntentionDetail

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
        self.lid1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            lid_text = "Choose",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.lid1.save()                                          
        self.lid2 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            lid_text = "Calculate",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.lid2.save()    
                     
    def test_learningIntention_create(self):
        """LearningIntention instance attributes are created OK"""
        
        self.assertEqual(self.learningintention1.lesson, self.lesson1)
        self.assertEqual(self.learningintention1.li_text, "Practise")
    
    def test_successCriterion_create(self):
        """SuccessCriterion instance attributes are created OK"""
        self.assertEqual(self.lid1.learning_intention, self.learningintention1)
        self.assertEqual(self.lid1.lid_text, "Choose")
        self.assertEqual(self.lid1.lid_type, LearningIntentionDetail.SUCCESS_CRITERION)
        
    def test_learningOutcome_create(self):
        """LearningOutcome instance attributes are created OK"""
        self.assertEqual(self.lid2.learning_intention, self.learningintention1)
        self.assertEqual(self.lid2.lid_text, "Calculate")
        self.assertEqual(self.lid2.lid_type, LearningIntentionDetail.LEARNING_OUTCOME)