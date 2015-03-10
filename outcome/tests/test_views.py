from django.test import TestCase
from courses.models import Course
from lesson.models import Lesson
from profile.models import User, Profile 
from interaction.models import UserCourse
from ..models import LearningIntention, LearningIntentionDetail

class OutcomeViewTests(TestCase):
    """Test the outcome specific views"""
    
    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   }
    lesson1_data = {
                    'name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
                   
    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.course1 = Course(**self.course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()        
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    text = "Practise")
        self.learningintention1.save()                                            
        self.lid1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Choose Topaz",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.lid1.save()  
        self.lid2 = LearningIntentionDetail(
            learning_intention = self.learningintention1,
            text = "Eat fish",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )                                        
        self.lid2.save()
        self.lid3 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Calculate 6*9",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.lid3.save()   
        
        self.profile1 = self.user1.profile
        self.profile1.accepted_terms = True
        self.profile1.signature_line = 'Learning stuff'
        self.profile1.save()
    
    def test_learning_intention(self):
        """Test view of a single learning intention"""
        
        les1 = self.lesson1.id
        lint1 = self.learningintention1.id
        url1 = "/lesson/{0}/lint/{1}/".format(les1,lint1)

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['lesson_id', 'lesson_intention_id'])
        self.assertIn("Choose Topaz", response.content, "SC missing")
        self.assertIn("Calculate 6*9", response.content, "LO missing")

        cycle1 = "cycle{0}".format(self.lid1.id)
        cycle2 = "cycle{0}".format(self.lid2.id)
        self.assertIn(cycle1, response.content, "Cycle button missing")
        self.assertIn(cycle2, response.content, "Cycle button missing")

        #test non-existing LI        
        response = self.client.get('/lesson/1/lint/5000/')
        self.assertEqual(response.status_code, 404)
        
        #test not logged in
        response = self.client.get(url1)
        self.assertNotIn('progressSC', response.context)
        
        ### Success Criteria Cycle Tests
        #press some buttons and see what happens
        self.client.login(username='bertie', password='bertword')
        #Register user on course first:
        uc = UserCourse(course=self.course1, user=self.user1)
        uc.save() 

        #cycle to amber        
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 1)
        self.assertInHTML("<img id='SC1' class='tl-red'>", response.content)
        self.assertEqual(response.context['progressSC'], (0,2,2,100)) #progress bar
        self.assertEqual(response.context['progressLO'], (0,1,1,100)) #progress bar

        #cycle to green
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 2)
        self.assertEqual(response.context['progressSC'], (1,1,2,100)) #progress bar
        self.assertEqual(response.context['progressLO'], (0,1,1,100)) #progress bar
    
        #cycle to red
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 0)
        self.assertEqual(response.context['progressSC'], (0,2,2,100)) #progress bar
        self.assertEqual(response.context['progressLO'], (0,1,1,100)) #progress bar
