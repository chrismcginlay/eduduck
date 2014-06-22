from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course
from lesson.models import Lesson
from ..models import LearningIntention, LearningIntentionDetail


class OutcomeModelTests(TestCase):
    """Test the models of the outcome app"""

    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   }
    lesson1_data = {'code': 'B1',
                    'name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
                   
    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()        
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    text = "Practise")
        self.learningintention1.save()                                            
        self.lid1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Choose",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.lid1.save()                                          
        self.lid2 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Calculate",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.lid2.save()    
                     
    def test_learningIntention_create(self):
        """LearningIntention instance attributes are created OK"""
        
        self.assertEqual(self.learningintention1.lesson, self.lesson1)
        self.assertEqual(self.learningintention1.text, "Practise")
    
    def test_learningIntention_get_absolute_url(self):
        """Test that LI return correct absolute url"""

        url = self.learningintention1.get_absolute_url()
        target = u"/lesson/{0}/lint/{1}/".format(
            self.lesson1.pk, self.learningintention1.pk)
        self.assertEqual(target, url, "course URL error")

    def test_successCriterion_create(self):
        """SuccessCriterion instance attributes are created OK"""
        self.assertEqual(self.lid1.learning_intention, self.learningintention1)
        self.assertEqual(self.lid1.text, "Choose")
        self.assertEqual(self.lid1.lid_type, LearningIntentionDetail.SUCCESS_CRITERION)
        
    def test_learningOutcome_create(self):
        """LearningOutcome instance attributes are created OK"""
        self.assertEqual(self.lid2.learning_intention, self.learningintention1)
        self.assertEqual(self.lid2.text, "Calculate")
        self.assertEqual(self.lid2.lid_type, LearningIntentionDetail.LEARNING_OUTCOME)
