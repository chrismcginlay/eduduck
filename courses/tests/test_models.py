"""
Unit tests for courses models
"""

import json
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from bio.models import Bio
from interaction.models import UserCourse
from outcome.models import LearningIntention, LearningIntentionDetail
from attachment.models import Attachment

from ..models import Course, Lesson, Video


class CourseModelTests(TestCase):
    """Test the models used to represent courses and constituent lessons etc"""

#TODO load data from JSON fixtures if these instances become irksome
#(in which case some of the assertions outwith loops over dicts 
#become redundant, which would be a good thing)

    course1_data = {
        'code': 'EDU02',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
        'level': 'Basic',
        'credits': 30,
    }
    course2_data = {
        'code': 'FBR9',
        'name': 'Basic Knitting',
        'abstract': 'Casting on',
        'level': '5',
        'credits': 20,
    }
    course3_data = {
        'code': 'PL1',
        'name': 'Public Speaking',
        'abstract': 'Talking in public',
        'level': 5,
        'credits': 15,
    }
    lesson1_data = {
        'code': 'B1',
        'name': 'Introduction to Music',
        'abstract': 'A summary of what we cover',
    }
    video1_data = {
        'url': 'http://youtu.be/LIM--jfnKeU',
        'name': 'Music introduction',
    }
    attachment1_data = {
        'name': 'Reading List',
        'desc': 'Useful stuff you might need',
        'seq': 3,
        'attachment': 'empty_attachment_test.txt',
    }
    attachment2_data = {
        'name': 'FAQ',
        'desc': 'Frequently Asked Questions',
        'seq': 3,
        'attachment': 'empty_attachment_test.txt',
    }
        
    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('hank', 'hank@example.com', 'hankdo')
        self.user2.is_active = True
        self.user2.save()
        self.bio1 = self.user1.bio
        self.bio1.accepted_terms = True
        self.bio1.signature_line = 'Learning stuff'
        self.bio1.user_tz = "Europe/Rome"
        self.bio1.save()
        self.bio2 = self.user2.bio
        self.bio2.accepted_terms = True
        self.bio2.signature_line = 'Tieing knots'
        self.bio2.user_tz = 'Atlantic/St_Helena'
        self.bio2.save()

        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user2
        self.course1.save()

        self.course2 = Course(**self.course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user2
        self.course2.save()

        self.course3 = Course(**self.course3_data)
        self.course3.organiser = self.user1
        self.course3.instructor = self.user2
        self.course3.save()

        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.video1 = Video(course=self.course1, **self.video1_data)
        self.video1.save()
        self.video2 = Video(lesson=self.lesson1, **self.video1_data)
        self.video2.save()
        self.attachment1 = Attachment(course=self.course1, 
                                      **self.attachment1_data)
        self.attachment1.save()
        self.attachment2 = Attachment(course=self.course3, 
                                      **self.attachment2_data)
        self.attachment2.save()
       
        self.learningintention1 = LearningIntention(lesson = self.lesson1, 
                                                    text = "Practise")
        self.learningintention1.save()                                            
        self.learningintentiondetail1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Choose",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.learningintentiondetail1.save()                                          
        self.learningintentiondetail2 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Calculate",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.learningintentiondetail2.save()                                        
        
    def test_course_create(self):
        """Course instance attributes are created OK"""
        for key,val in self.course1_data.items():
            self.assertEqual(self.course1.__dict__[key], val)
    
    def test_course_get_absolute_url(self):
        """Course returns correct get_absolute_url"""
        
        url = self.course1.get_absolute_url()
        target = u"/courses/%s/" % self.course1.pk
        self.assertEqual(target, url, "course URL error")
    
    def test_lesson_get_absolute_url(self):
        """Lesson returns correct get_absolute_url"""

        url = self.lesson1.get_absolute_url()
        target = u"/courses/{0}/lesson/{1}/".format(self.lesson1.course.pk,self.lesson1.pk)
        self.assertEqual(target, url, "lesson URL error")

    def test_lesson_create(self):
        """Lesson instance attributes are created OK"""
        for key,val in self.lesson1_data.items():
            self.assertEqual(self.lesson1.__dict__[key], val)
        self.assertEqual(self.lesson1.course, self.course1)
            
    def test_video_create(self):
        """Video instance attributes are created OK"""
        #Associated with course
        for key,val in self.video1_data.items():
            self.assertEqual(self.video1.__dict__[key], val)
        self.assertEqual(self.video1.course, self.course1)
            
        #Associated with lesson
        for key,val in self.video1_data.items():
            self.assertEqual(self.video2.__dict__[key], val)
        self.assertEqual(self.video2.lesson, self.lesson1)
            
    def test_attachment_create(self):
        """Attachment instance attributes are created OK"""
        for key,val in self.attachment1_data.items():
            self.assertEqual(self.attachment1.__dict__[key], val)   
        self.assertEqual(self.attachment1.course, self.course1)
          
