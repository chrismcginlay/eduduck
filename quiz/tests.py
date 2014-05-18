"""
Unit tests for Courses app
"""

from unittest import skip
from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from .models import (Answer, Quiz, Question,  QuizAttempt, QuestionAttempt)

@skip("")
class QuizModelTests(TestCase):
    """Test the models used to represent quizzes"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    answer1_data = {'answer_text': "Hot",
                    'explan_text' : "Incandescent gas emits light",
                    }
    answer2_data = {'answer_text' : "Cold",
                    'explan_text' : "Nope"
                    }                    
    
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.answer1 = Answer(**self.answer1_data)
        self.answer1.save()
        self.answer2 = Answer(**self.answer2_data)
        self.answer2.save()
        self.question1 = Question(question_text = "Describe a flame",
                                  correct_answer = self.answer1)
        self.question1.save()
        self.question1.answers.add(self.answer1) 
        self.question1.answers.add(self.answer2)
        self.question1.save()
        
    def test_answer_create(self):
        """Answer instance attributes are created OK"""
        for key,val in self.answer1_data.items():
            self.assertEqual(self.answer1.__dict__[key], val)
    
    def test_question_create(self):
        """Question instance attributes are created OK"""
        q = self.question1
        self.assertEqual(q.question_text, "Describe a flame")
        self.assertEqual(q.answers.all()[0], self.answer1)
        self.assertEqual(q.answers.all()[1], self.answer2)
        self.assertEqual(q.correct_answer, self.answer1)
            
   
class QuizViewTests(TestCase):
    """Test the quiz views"""
    
    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 4,
                   'course_credits': 30,
                   }
    lesson1_data = {'lesson_code': 'B1',
                    'lesson_name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
    answer1_data = {'answer_text': "Hot",
                    'explan_text' : "Incandescent gas emits light",
                    }
    answer2_data = {'answer_text' : "Cold",
                    'explan_text' : "Nope"
                    }     
                    
    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.answer1 = Answer(**self.answer1_data)
        self.answer1.save()
        self.answer2 = Answer(**self.answer2_data)
        self.answer2.save()
        self.question1 = Question(question_text = "Describe a flame",
                                  correct_answer = self.answer1)
        self.question1.save()
        self.question1.answers.add(self.answer1) 
        self.question1.answers.add(self.answer2)
        self.question1.save()
        
    @skip("")
    def test_quiz_take_index(self):
        """Check quiz index page loads OK and has correct variables"""
        response = self.client.get('/quiz_take/1')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        self.assertTrue(x in response.context for x in ['quiz', 
                                                        'error_message'])
            