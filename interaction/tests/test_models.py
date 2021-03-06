#interaction/tests/test_models.py

import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils.timezone import is_aware
from django.contrib.auth.models import User

from core.eduduck_exceptions import CheckRepError
from outcome.models import LearningIntention, LearningIntentionDetail
from courses.models import Course
from lesson.models import Lesson
from attachment.models import Attachment
from ..models import (
    UserCourse, 
    UserLesson,
    UserLearningIntention,
    UserLearningIntentionDetail, 
    ULIDConditions,
    UserAttachment,
    UAActions
)

course1_data = {'code': 'EDU02',
               'name': 'A Course of Leeches',
               'abstract': 'Learn practical benefits of leeches',
               }

course2_data = {'code': 'EDU03',
               'name': 'The Coarse and The Hoarse',
               'abstract': 'High volume swearing leading to loss of voice',
               }
course3_data = {'code': 'EDU04',
               'name': 'Pie Eating',
               'abstract': 'Gut Busting leads to Butt Gusting',
               }
course4_data = {'code': 'EDU05',
               'name': 'Golk',
               'abstract': 'The Contact Sport',
               }

class UserCourseModelTests_2(TestCase):
    """Test model representing user interaction with courses.

    This class uses fixtures, unlike the original one below.
    Add new tests here.
    """

    fixtures = [
        'auth_user.json', 
        'courses.json',
        'lessons.json',
        'outcome_lints.json',
        'interactions.json',
    ]

    def test__checkrep_flags_enrolled_user_also_organiser(self):
        """Course organiser or instructor shouldn't be enrolling in course!"""

        # Detect conflicted enrollment
        interaction = UserCourse.objects.get(pk=3)
        interaction.user = interaction.course.organiser #conflicts 
        self.assertFalse(interaction._checkrep())

        # Allow non-conflicted enrollment:
        interaction = UserCourse.objects.get(pk=1)
        self.assertTrue(interaction._checkrep())

         
class UserCourseModelTests(TestCase):
    """Test models user interaction with courses"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()

        self.user2 = User.objects.create_user('flo', 'flo@example.com', 'flo')
        self.user2.is_active = True
        self.user2.save()

        self.course1 = Course(**course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()
        self.course2 = Course(**course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user1
        self.course2.save()
        self.course3 = Course(**course3_data)
        self.course3.instructor = self.user1
        self.course3.organiser = self.user1
        self.course3.save()
        self.course4 = Course(**course4_data)
        self.course4.instructor = self.user1
        self.course4.organiser = self.user1
        self.course4.save()

        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.uc2 = UserCourse(course=self.course2, user=self.user2)
        self.uc2.save()
        self.uc3 = UserCourse(course=self.course3, user=self.user2)
        self.uc3.save()

    # Test states of flags 'active' 'completed' 'withdrawn' or ACW
    # ACW, AC-, A-W, -CW, --- Error
    # A--, -C-, --W OK
    def test__checkrep_enrol_flags_OK(self):
        # new uc, activated by save() method
        self.assertTrue(self.uc.active)
        self.assertFalse(self.uc.completed)
        self.assertFalse(self.uc.withdrawn)
        self.assertTrue(self.uc._checkrep())
       
    def test__checkrep_complete_flags_OK(self):
        self.uc.complete()
        self.assertFalse(self.uc.active)
        self.assertTrue(self.uc.completed)
        self.assertFalse(self.uc.withdrawn)
        self.assertTrue(self.uc._checkrep())
    
    def test__checkrep_withdrawn_flags_OK(self):
        self.uc.withdraw()
        self.assertFalse(self.uc.active)
        self.assertFalse(self.uc.completed)
        self.assertTrue(self.uc.withdrawn)
        self.assertTrue(self.uc._checkrep())

    def test__checkrep_flags_Error(self):
        with self.assertRaises(CheckRepError):
            self.uc.active = True
            self.uc.completed = True
            self.uc.withdrawn = True
            self.uc._checkrep()
        with self.assertRaises(CheckRepError):
            self.uc.active = True
            self.uc.completed = True
            self.uc.withdrawn = False
            self.uc._checkrep()
        with self.assertRaises(CheckRepError):
            self.uc.active = True
            self.uc.completed = False 
            self.uc.withdrawn = True
            self.uc._checkrep()
        with self.assertRaises(CheckRepError):
            self.uc.active = False
            self.uc.completed = True
            self.uc.withdrawn = True
            self.uc._checkrep()
        with self.assertRaises(CheckRepError):
            self.uc.active = False
            self.uc.completed = False
            self.uc.withdrawn = False
            self.uc._checkrep()

    def test_usercourse_create(self):
        """Test creating new row with course 2"""

        self.assertTrue(self.uc2.pk, "Failed to create new db entry")
        self.assertTrue(self.uc2._checkrep(), "_checkrep failed")

    def test_hist2list(self):
        """Test conversion of JSON encoded history to tuple list with course 3"""

        self.uc3.withdraw()
        self.uc3.reopen()
        self.uc3.complete()

        h2l_output = self.uc3.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, 
                                  "Should be a datetime")
            self.assertTrue(is_aware(row[0]), "Datetime not TZ aware")
            self.assertIsInstance(row[1], str, "Action should be a string")

        #Now check the history messages in reverse order.
        last = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', 
                         "Action should be DEACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'COMPLETION', "Action should be COMPLETION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Action should be ACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REOPENING', "Action should be REOPENING")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', 
                         "Action should be DEACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'WITHDRAWAL', "Action should be WITHDRAWAL")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Action should be ACTIVATION")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REGISTRATION', 
                         "Action should be REGISTRATION")

             
    def test_withdraw(self):
        """Test the course withdraw method"""

        self.uc.withdraw()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'WITHDRAWAL', "Wrong action in history")
        self.assertEqual(self.uc.active, False, "Should not be active")
        self.assertEqual(self.uc.withdrawn, True, "Should be withdrawn")
        self.assertEqual(self.uc.completed, False, "Should not be completed")
       
    def test_reopen(self):
        """Test the course reopen method"""

        self.uc.complete() 
        self.uc.reopen()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'ACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'REOPENING', "Wrong action in history")
        self.assertEqual(self.uc.active, True, "Should be active")
        self.assertEqual(self.uc.withdrawn, False, "Should not be withdrawn")
        self.assertEqual(self.uc.completed, False, "Should not be completed")
       
    def test_complete(self):
        """Test the course complete method"""

        self.uc.complete()
        h2l_output = self.uc.hist2list()
        last = h2l_output.pop()
        last2 = h2l_output.pop()
        self.assertEqual(last[1], 'DEACTIVATION', "Wrong action in history")
        self.assertEqual(last2[1], 'COMPLETION', "Wrong action in history")
        self.assertEqual(self.uc.active, False, "Should not be active")
        self.assertEqual(self.uc.withdrawn, False, "Should not be withdrawn")
        self.assertEqual(self.uc.completed, True, "Should be completed")
   
    def test_get_status(self):
        """Test that the correct status is returned"""

        self.assertEqual(self.uc.get_status(), 'active', 
                         "Status should be 'active'")
        self.uc.complete()
        self.assertEqual(self.uc.get_status(), 'completed', 
                         "Status should be 'completed'")
        self.uc.reopen()
        self.assertEqual(self.uc.get_status(), 'active', 
                         "Status should be 'active'")
        self.uc.withdraw()
        self.assertEqual(self.uc.get_status(), 'withdrawn', 
                         "Status should be 'withdrawn'")
       
    def test___str__(self):
        """Test that the desired info is in the unicode method"""
        s = self.uc3.__str__()
        self.assertIn(self.uc3.user.username, s, 
                      "The username should be in the unicode")
        self.assertIn(self.uc3.course.name, s, 
                      "The course_name should be in the unicode")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""
        unicod = self.uc3.__unicode__()
        s = u"UC:%s, User:%s, Course:%s" % \
            (self.uc3.pk, self.uc3.user.pk, self.uc3.course.pk)
        self.assertEqual(unicod, s, "Unicode output failure")

    def test_get_absolute_url(self):
        """Test the correct url is returned"""

        url = self.uc3.get_absolute_url()
        u = self.uc3.user.pk
        c = self.uc3.course.pk
        s = u"/interaction/user/%s/course/%s/"% (u,c)
        self.assertEqual(s, url, "URL error")


class UserLessonModelTests(TestCase):
    """Test models user interaction with lessons"""

    def setUp(self):
        #set up courses, one user, enrol the user on course1, but not course2
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()

        self.user2 = User.objects.create_user('flo', 'flo@example.com', 'flo')
        self.user2.is_active = True
        self.user2.save()
        self.course1 = Course(**course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()
        self.course2 = Course(**course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user1
        self.course2.save()
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson1 = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson1.save()
        self.ul = UserLesson(user=self.user2, lesson=self.lesson1)
        self.ul.save()
        self.lesson2 = Lesson(name="Test Lesson 2", course = self.course1)
        self.lesson2.save()
        self.ul2 = UserLesson(user=self.user2, lesson=self.lesson2)
        self.ul2.save()
        self.lesson3 = Lesson(name="Test Lesson 3", course = self.course1)
        self.lesson3.save()
        self.ul3 = UserLesson(user=self.user2, lesson=self.lesson3)
        self.ul3.save()

        self.lesson4 = Lesson(name="Test Lesson 4, in course 2", course = self.course2)
        self.lesson4.save()


    def test_checkrep(self):
        """Test the internal representation checker with lesson 1"""

        self.assertTrue(self.ul._checkrep(), 
            "First visit to lesson - checkrep failed")
        self.ul.visited = False
        self.ul.completed = False
        with self.assertRaises(CheckRepError):
            self.ul._checkrep()
        
        self.ul.visited = False
        self.ul.completed = True
        with self.assertRaises(CheckRepError):
            self.ul._checkrep()

        self.ul.visited = True
        self.ul.completed = False
        self.assertTrue(self.ul._checkrep(), "Checkrep false failure")

        self.ul.visited = True
        self.ul.completed = True
        self.assertTrue(self.ul._checkrep(), "Checkrep false failure")

        self.ul.completed = False
        self.ul.complete()
        self.assertTrue(self.ul2._checkrep(), "Checkrep false failure")

        self.ul.completed = False
        self.assertFalse(self.ul._checkrep(), 
            "Checkrep didn't pick up failing state")

    # Test states of flags 'visited' 'completed' or VC
    # --, -C would be Error state
    # VC, V- OK
    def test__checkrep_VC_flags_OK(self):
        # new ul, activated by save() method
        self.ul.complete()
        self.assertTrue(self.ul.completed)
        self.assertTrue(self.ul.visited)
        self.assertTrue(self.ul._checkrep())
       
    def test__checkrep_V_flags_OK(self):
        self.assertTrue(self.ul.visited)
        self.assertFalse(self.ul.completed)
        self.assertTrue(self.ul._checkrep())
    
    def test__checkrep_False_flags_Error(self):
        self.ul.visited = False
        self.ul.completed = False
        with self.assertRaises(CheckRepError):
            self.ul._checkrep()

    def test__checkrep_flags_Error(self):
        self.ul.completed = True
        self.ul.visited = False
        with self.assertRaises(CheckRepError):
            self.ul._checkrep()

    def test_userlesson_create(self):
        """Test creating new row with lesson 2 and 4"""

        self.assertTrue(self.ul2.pk, "Failed to create new db entry")
        self.assertTrue(self.ul2._checkrep(), "_checkrep failed")

        #userlesson for lesson 4 should fail, as not enrolled on course2
        ul4 = UserLesson(user=self.user1, lesson=self.lesson4)
        ul4.save()
        self.assertIsNone(ul4.pk)

    def test_hist2list(self):
        """Test conversion of JSON encoded history to tuple list with course 3"""

        self.ul3.complete()
        self.ul3.reopen()
        self.ul3.complete()

        h2l_output = self.ul3.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, 
                                  "Should be a datetime")
            self.assertTrue(is_aware(row[0]), "Datetime not TZ aware")
            self.assertIsInstance(row[1], str, "Action should be a string")

        #Now check the history messages in reverse order.
        last = h2l_output.pop()
        self.assertEqual(last[1], 'COMPLETING', "Action should be COMPLETING")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REOPENING', "Action should be REOPENING")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'COMPLETING', "Action should be COMPLETING")
        last = h2l_output.pop()
        self.assertEqual(last[1], 'VISITING', "Action should be VISITING")

    def test_reopen(self):
        """Test the lesson reopen method"""

        self.ul.complete() 
        self.ul.reopen()
        h2l_output = self.ul.hist2list()
        last = h2l_output.pop()
        self.assertEqual(last[1], 'REOPENING', "Wrong action in history")
        self.assertEqual(self.ul.visited, True, "Visited should be set")
        self.assertEqual(self.ul.completed, False, 
                         "Completed should not be set")

    def test_complete(self):
        """Test the lesson complete method"""

        self.ul.complete()
        h2l_output = self.ul.hist2list()
        last = h2l_output.pop()
        self.assertEqual(last[1], 'COMPLETING', "Wrong action in history")
        self.assertEqual(self.ul.visited, True, "Visited should be set")
        self.assertEqual(self.ul.completed, True, "Completed should be set")

    def test_visit(self):
        """Test visiting lessons"""

        self.ul.visit()
        h2l_output = self.ul.hist2list()
        last = h2l_output.pop()
        self.assertEqual(last[1], 'VISITING', "Wrong action in history")
        self.assertEqual(self.ul.visited, True, "Visited should be set")

        #The following should not produce a database record.
        #The user is not enrolled on the corresponding course.
        #ul4 = UserLesson(user=self.user1, lesson=self.lesson4)
        #ul4.visit() #can't run test, visit() asserts on failed _checkrep (as it should)
        #self.assertIsNone(ul4.pk)

    def test_get_status(self):
        """Test that the correct status is returned"""

        self.assertEqual(self.ul.get_status(), 'visited', 
                         "Status should be 'active'")
        self.ul.complete()
        self.assertEqual(self.ul.get_status(), 'completed', 
                         "Status should be 'completed'")
        self.ul.reopen()
        self.assertEqual(self.ul.get_status(), 'visited', 
                         "Status should be 'active'")

    def test___str__(self):
        """Test that the desired info is in the unicode method"""

        s = self.ul3.__str__()
        self.assertIn(self.ul3.user.username, s, 
                      "The username should be in the unicode")
        self.assertIn(self.ul3.lesson.name, s, 
                      "The lesson_name should be in the unicode")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""

        unicod = self.ul3.__unicode__()
        s = u"UL:%s, User:%s, Lesson:%s" % \
            (self.ul3.pk, self.ul3.user.pk, self.ul3.lesson.pk)
        self.assertEqual(unicod, s, "Unicode output failure")

    def test_get_absolute_url(self):
        """Test the correct url is returned"""

        url = self.ul3.get_absolute_url()
        u = self.ul3.user.pk
        l = self.ul3.lesson.pk
        s = u"/interaction/user/%s/lesson/%s/"% (u,l)
        self.assertEqual(s, url, "URL error")
       
       
class UserLearningIntentionModelTests(TestCase):
    """Test model behaviour of user interaction with learning intentions"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()   

        self.user2 = User.objects.create_user('flo', 'flo@example.com', 'flo')
        self.user2.is_active = True
        self.user2.save()
 
        self.course1 = Course(**course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save() 
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson.save() 
        self.li = LearningIntention(lesson=self.lesson, text="Intend...")
        self.li.save()
        self.uli = UserLearningIntention(user=self.user2, 
                                         learning_intention = self.li)
        self.lid1 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID A",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid2 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID B",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid3 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID C",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid4 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID D",
            lid_type=LearningIntentionDetail.LEARNING_OUTCOME)
        self.lid5 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID E",
            lid_type=LearningIntentionDetail.LEARNING_OUTCOME)
        self.lid6 = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="LID F",
            lid_type=LearningIntentionDetail.LEARNING_OUTCOME)
        self.lid1.save()
        self.lid2.save()
        self.lid3.save()
        self.lid4.save()
        self.lid5.save()
        self.lid6.save()
        self.ulid1 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid1)
        self.ulid1.save()    
        self.ulid2 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid2)
        self.ulid2.save()
        self.ulid3 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid3)
        self.ulid3.save()
        self.ulid4 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid4)
        self.ulid4.save()
        self.ulid5 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid5)
        self.ulid5.save()
        self.ulid6 = UserLearningIntentionDetail(user=self.user2,
                                    learning_intention_detail=self.lid6)
        self.ulid6.save()

    def test___unicode__(self):
        self.assertEqual(u"ULI:%s, User:%s, LI:%s" % \
            (self.uli.pk, self.user2.pk, self.li.pk), self.uli.__unicode__())        

    def test___str__(self):
        self.assertEqual(u"User %s's data for LI:%s..." % \
            (self.user2.username, self.li.text[:10]), self.uli.__str__())

    def test_progress(self):
        self.assertEqual(self.uli.progress(), {u'SC':(0,3), u'LO':(0,3)})
        self.ulid1.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(0,3), u'LO':(0,3)})
        self.ulid1.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(1,3), u'LO':(0,3)})        
        self.ulid4.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(1,3), u'LO':(0,3)})
        self.ulid4.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(1,3), u'LO':(1,3)})
        self.ulid2.cycle()
        self.ulid2.cycle()
        self.ulid3.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(2,3), u'LO':(1,3)})
        self.ulid3.cycle()
        self.ulid4.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(3,3), u'LO':(0,3)})
        self.ulid5.cycle()
        self.ulid5.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(3,3), u'LO':(1,3)})
        self.ulid6.cycle()
        self.ulid6.cycle()
        self.assertEqual(self.uli.progress(), {u'SC':(3,3), u'LO':(2,3)})


class UserLearningIntentionDetailModelTests(TestCase):
    """Test model behaviour of user interaction with 
    learning intention details"""

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()    
        
        self.user2 = User.objects.create_user('flo', 'flo@example.com', 'flo')
        self.user2.is_active = True
        self.user2.save()
        
        self.course1 = Course(**course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save() 
        self.course2 = Course(**course2_data)
        self.course2.instructor = self.user1
        self.course2.organiser = self.user1
        self.course2.save()
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson.save()
        self.lesson2 = Lesson(name="Test Lesson 2", course = self.course2)
        self.lesson2.save()
        self.li = LearningIntention(lesson=self.lesson, text="Intend...")
        self.li2 = LearningIntention(lesson=self.lesson2, text="Explore...")
        self.li.save()
        self.li2.save()
        self.lid = LearningIntentionDetail(
            learning_intention=self.li, 
            text ="Criterion...",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid2 = LearningIntentionDetail(
            learning_intention=self.li2, 
            text ="Criterion...",
            lid_type=LearningIntentionDetail.SUCCESS_CRITERION)
        self.lid.save()
        self.lid2.save()
        self.ulid = UserLearningIntentionDetail(
            user=self.user2, learning_intention_detail=self.lid)
        self.ulid.save()

    def test_cycling_first_click_on_a_LID_triggers_save(self):
        """When user first clicks on a LID, a ULID needs a primary key

        The first time a user clicks on a LID (learning intention detail),
        a ULID interaction will be created in memory by the view
        userlearningintentiondetail_cycle, having no PK. The model cycle()
        should check and save to the database if this is the first click."""


        # Enrol user on course 2:
        UserCourse(course=self.course2, user=self.user2).save()
        # Simulate first click on LID:
        ulid_mem = UserLearningIntentionDetail(
            user=self.user2, learning_intention_detail=self.lid2)
        self.assertFalse(ulid_mem.pk)
        ulid_mem.cycle()
        self.assertTrue(ulid_mem.pk)   

    def test__checkrep_passes_initial_state(self):
        """Test the internal representation checker with LID interaction"""

        self.assertTrue(self.ulid._checkrep(), "ULID _checkrep failed")
        
    def test__checkrep_picks_up_errored_initial_states(self):
        self.ulid.condition = ULIDConditions.amber #errored state
        self.assertFalse(self.ulid._checkrep())
        self.ulid.condition = ULIDConditions.green #errored state
        self.assertFalse(self.ulid._checkrep())

    def test__checkrep_picks_up_nonsense_conditions(self):
        self.ulid.condition = None
        with self.assertRaises(CheckRepError):
            self.ulid._checkrep()
        self.ulid.condition = "topaz"
        with self.assertRaises(CheckRepError):
            self.ulid._checkrep()
        
    def test_save(self):
        """Test the save functionality

        Principally, it should not save unless the user is enrolled
        on the corresponding course"""
        ulid2 = UserLearningIntentionDetail(user=self.user1,
                                    learning_intention_detail=self.lid2)
        ulid2.save()
        self.assertIsNone(ulid2.pk)	#should fail, user not on corr. course


    def test_cycle(self):
        """Check that state cycling works"""

        self.assertTrue(self.ulid._checkrep(), "Failure prior to cycle")
        self.assertEqual(self.ulid.condition, ULIDConditions.red)
        self.ulid.cycle()
        self.assertTrue(self.ulid._checkrep(), "Fail after first cycle")
        self.assertEqual(self.ulid.condition, ULIDConditions.amber)
        self.ulid.cycle()
        self.assertTrue(self.ulid._checkrep(), "Fail after second cycle")
        self.assertEqual(self.ulid.condition, ULIDConditions.green)
        self.ulid.cycle()
        self.assertTrue(self.ulid._checkrep(), "Fail after third cycle")
        self.assertEqual(self.ulid.condition, ULIDConditions.red)

    def test_cycle_history_timebar(self):
        """Test 5 minute timebar on history updates

        History of cycling events should append a new event if over 5 mins
        have elapsed since the last event, otherwise replace last history.
        """

        self.assertTrue(self.ulid._checkrep(), "Failure prior to cycle")
        #First check that rapid successive cycles don't append to history, 
        #intead, last entry should be replaced
        #NB: ulid.hist is JSON string. Count hist2list elements instead
        self.ulid.cycle()
        count1 = len(self.ulid.hist2list())  
        self.ulid.cycle()
        count2 = len(self.ulid.hist2list())
        self.assertEqual(count2, count1, "History grew when it shouldn't have")

        #Doctor the date to 10 mins prior, 
        #check that subsequent cycle does append to history        
        hist = json.loads(self.ulid.history)
        last_event = hist.pop()
        last_time = last_event[0]
        last_time = last_time - 600 #600 seconds earlier
        hist.append((last_time, last_event[1]))
        self.ulid.history = json.dumps(hist)
        self.ulid.cycle()
        count3 = len(self.ulid.hist2list())
        self.assertGreater(count3, count2, 
                           "History did not grow when it should")


    def test_hist2list(self):
        """See that history converts to list properly"""

        h2l_output = self.ulid.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, 
                                  "Should be a datetime")
            self.assertTrue(is_aware(row[0]), "Datetime not TZ aware")
            self.assertIsInstance(row[1], str, "Action should be a string")

        last = h2l_output.pop()
        self.assertEqual(last[1], 'SET_RED', "Action should be SET_RED")


    def test_get_status(self):
        """Test that the correct status is returned"""

        self.assertEqual(self.ulid.get_status(), 'red', 
                         "Status should be 'red'")
        self.ulid.cycle()
        self.assertEqual(self.ulid.get_status(), 'amber', 
                         "Status should be 'amber'")
        self.ulid.cycle()
        self.assertEqual(self.ulid.get_status(), 'green', 
                         "Status should be 'green'")
        self.ulid.cycle()
        self.assertEqual(self.ulid.get_status(), 'red', 
                         "Status should be 'red'")

    def test___str__(self):
        """Test that the desired info is in the unicode method"""
        s = self.ulid.__str__()
        self.assertIn(self.ulid.user.username, s, 
                      "The username should be in the unicode")
        self.assertIn(self.ulid.learning_intention_detail.text[:10], s, 
                      "The first 10 chars of the criterion_text "
                      "should be in the unicode")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""
        unicod = self.ulid.__unicode__()
        s = u"ULID:%s, User:%s, LID:%s" % \
            (self.ulid.pk, self.ulid.user.pk, 
             self.ulid.learning_intention_detail.pk)
        self.assertEqual(unicod, s, "Unicode output failure")

class UserAttachmentModelTests(TestCase):
    """Test model behaviour of user interaction with attachments"""
    
    att1_data = {
        'name': 'Reading List',
        'desc': 'Useful stuff you might need',
        'seq': 3,
        'attachment': 'empty_attachment_test.txt',
    }
    att2_data = {
        'name': 'Grammer Guide',
        'desc': 'How do you even spell grammer?',
        'seq': 2,
        'attachment': 'empty_attachment_test.txt',
    }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                             'bertword')
        self.user1.is_active = True
        self.user1.save()    

        self.user2 = User.objects.create_user('flo', 'flo@example.com', 'flo')
        self.user2.is_active = True
        self.user2.save()

        self.course1 = Course(**course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save() 
        self.course2 = Course(**course2_data)
        self.course2.instructor = self.user1
        self.course2.organiser = self.user1
        self.course2.save()
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        self.lesson1 = Lesson(name="Test Lesson 1", course = self.course1)
        self.lesson1.save()
        self.lesson2 = Lesson(name="Test Lesson 2", course = self.course2)
        self.lesson2.save()
        #att1 attached to course
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att1.save()      
        #att2 attached to lesson
        self.att2 = Attachment(lesson=self.lesson1, **self.att1_data)
        self.att2.save()   
        #att3 attached to lesson in course2
        self.att3 = Attachment(lesson=self.lesson2, **self.att1_data)
        self.att3.save()

        self.u_att1 = UserAttachment(attachment=self.att1, user=self.user2)
        self.u_att2 = UserAttachment(attachment=self.att2, user=self.user2)
        self.u_att1.save()
        self.u_att2.save()        
       
    def test_hist2list(self):
        """Test conversion of JSON encoded history to tuple list"""

        #History will need some activity to test. Since model doesn't need a
        #download method, best to create this in views via client        
        self.client.login(username='flo', password='flo')
        response = self.client.get('/interaction/attachment/1/download')
        assert(response)
        response = self.client.get('/interaction/attachment/1/download')
        h2l_output = self.u_att1.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, 
                                  "Should be a datetime")
            self.assertTrue(is_aware(row[0]), "Datetime not TZ aware")
            self.assertIn(row[1], UAActions, 
                          "Action should be DOWNLOADING etc")
                            
    def test__checkrep(self):
        #TODO test the history checking in _checkrep
        self.fail("write me") 

    def test___unicode__(self):
        self.assertEqual(
            u"UA:%s, User:%s, Attachment:%s" % \
            (self.u_att2.pk, self.user2.pk, self.att2.pk), 
            self.u_att2.__unicode__())        
       
    def test___str__(self):
        t = u"User {0}'s data for attachment: ...{1}" \
            .format(self.user2.username, str(self.att1.attachment)[-10:])
        s = self.u_att2.__str__()
        self.assertEqual(s, t)
   
    def test_get_absolute_url(self):
        t = u"/interaction/attachment/{0}/download/".format(self.att1.pk)
        url = self.u_att1.get_absolute_url()
        self.assertEqual(t,url) 
                         
    def test_save(self):
        """Test that save only saves when user is enrolled on course"""
        
        u_att3 = UserAttachment(attachment=self.att3, user=self.user2)
        u_att3.save()
        self.assertIsNone(u_att3.pk)
