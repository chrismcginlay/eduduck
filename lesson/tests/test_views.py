# Unit tests for lesson views

from datetime import datetime
from django.test import TestCase

from lesson.models import Lesson

class LessonViewTests(TestCase):
    
    def test_lesson_unauth(self):
        """Test view of single lesson for unauthenticated user"""
        
        c1 = self.course1.pk
        l1 = self.lesson1.pk
        url1 = '/courses/{0}/lesson/{1}/'.format(c1,l1)
        
        self.client.logout()        
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
                        for x in ['course', 'lesson', 'ul', 'attachments',
                        'history', 'learning_intentions'])
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - unauthenticated")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - unauthenticated")                 
        
        def test_course_lesson_auth(self):
            """Test view of single lesson for authenticated user"""
            
            self.client.login(username='bertie', password='bertword')        
            c1 = self.course1.pk
            l1 = self.lesson1.pk
            url1 = '/courses/{0}/lesson/{1}/'.format(c1, l1)
        c3 = self.course3.pk
        l2 = self.lesson2.pk
        url3 = '/courses/{0}/lesson/{1}/'.format(c3, l2)
        
        #First for user who is registered on course
        uc = UserCourse(course=self.course1, user=self.user1)
        uc.save()
        response = self.client.get(url1)
        
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.status_code, 200)
        hist = response.context['history'].pop()
        self.assertIsInstance(hist[0], datetime, 
                              "Problem with lesson history timestamp")
        self.assertEqual(hist[1], 'VISITING', 
                         "Problem with lesson history activity")
        
        self.assertNotEqual(response.context['ul'], None, 
                            "There should be a userlesson - authenticated")                 
        #see that lesson complete button works 
        response = self.client.post(url1, {'lesson_complete':'Complete'})
        self.assertIn('lesson_reopen', response.content)
        self.assertEqual(response.context['ul'].completed, True) 
        
        #see that lesson reopen button works 
        response = self.client.post(url1, {'lesson_reopen':'Re-open'})
        self.assertIn('lesson_complete', response.content)
        self.assertEqual(response.context['ul'].completed, False)        
        
        #then check context for user not registered on course
        response = self.client.get(url3)
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - unregistered")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - unregistered")  