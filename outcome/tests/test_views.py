from django.test import TestCase
from courses.models import Course, Lesson
from bio.models import User, Bio
from interaction.models import UserCourse
from ..models import LearningIntention, LearningIntentionDetail
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
        self.lid1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            lid_text = "Choose Topaz",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.lid1.save()  
        self.lid2 = LearningIntentionDetail(
            learning_intention = self.learningintention1,
            lid_text = "Eat fish",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )                                        
        self.lid2.save()
        self.lid3 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            lid_text = "Calculate 6*9",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.lid3.save()   
        
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.bio1 = Bio.objects.get(user_id=1)
        self.bio1.accepted_terms = True
        self.bio1.signature_line = 'Learning stuff'
        self.bio1.save()
    
    def test_learning_intention(self):
        """Test view of a single learning intention"""
        
        response = self.client.get('/lesson/1/lint/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['lesson_id', 'lesson_intention_id'])
        self.assertIn("Choose Topaz", response.content, "SC missing")
        self.assertIn("Calculate 6*9", response.content, "LO missing")
        self.assertIn("cycle1", response.content, "Cycle button missing")
        self.assertIn("cycle2", response.content, "Cycle button missing")

        #test non-existing LI        
        response = self.client.get('/lesson/1/lint/5/')
        self.assertEqual(response.status_code, 404)
        
        ### Success Criteria Cycle Tests
        #press some buttons and see what happens
        self.client.login(username='bertie', password='bertword')
        #Register user on course first:
        uc = UserCourse(course=self.course1, user=self.user1)
        uc.save() 

        #cycle to amber        
        response = self.client.post('/lesson/1/lint/1/', {'cycle1':'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 1)
        
        #cycle to green
        response = self.client.post('/lesson/1/lint/1/', {'cycle1':'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 2)
    
        #cycle to red
        response = self.client.post('/lesson/1/lint/1/', {'cycle1':'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 0)