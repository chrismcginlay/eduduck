import datetime
from timezone import is_aware

from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from interaction.models import UserCourse, UserLesson

class AttachmentModelTests(TestCase):
    """Test models user interaction with courses"""

    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 'Basic',
                   'course_credits': 30,
                   }

    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        
        self.att1 = Attachment.objects.create()
        
    def test_checkrep(self):
        """Test the internal representation checker with attachments"""
        self.assert_(self.uc._checkrep(), "New attachment checkrep failed")

    def test_hist2list(self):
        """Test conversion of JSON encoded history to tuple list"""
       
        self.fail("Do stuff with the attachment to create history")        
        h2l_output = self.att1.hist2list()
        self.assertIsInstance(h2l_output, list, "Output should be a list")
        for row in h2l_output:
            self.assertIsInstance(row, tuple, "Entry should be a tuple")
            self.assertIsInstance(row[0], datetime.datetime, 
                                  "Should be a datetime")
            self.assertTrue(is_aware(row[0]), "Datetime not TZ aware")
            self.assertIsInstance(row[1], str, "Action should be a string")
            
        #Now check the history messages in reverse order.
        last = h2l_output.pop()
        self.assertEqual(last[1], 'DOWNLOADED', 
                         "Action should be DOWNLOADED")
                              
    def test___str__(self):
        """Test that the desired info is in the unicode method"""
        s = self.att1.__str__()
        self.assertIn(self.att1.user.username, s, 
                      "The username should be in the unicode")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""
        unicod = self.att1.__unicode__()
        s = u"UC:%s, User:%s, Course:%s" % \
            (self.uc3.pk, self.uc3.user.pk, self.uc3.course.pk)
        self.assertEqual(unicod, s, "Unicode output failure")

    def test_get_absolute_url(self):
        """Test the correct url is returned"""
        
        url = self.att1.get_absolute_url()
        the_user = self.user1.pk
        the_att = self.att1.pk
        s = "/interaction/user/%s/attachment/%s/download"% (the_att, the_user)
        self.assertEqual(s, url, "attachment URL error")
        
    def test_get_metadata_url(self):
        """Test that the correct metadata url is returned"""
        
        self.fail