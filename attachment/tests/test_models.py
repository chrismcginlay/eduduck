from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course
from lesson.models import Lesson
from interaction.models import UserCourse

from ..models import Attachment

class AttachmentModelTests(TestCase):
    """Test models user interaction with courses"""

    course1_data = {
        'code': 'EDU01',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
        'level': 'Basic',
        'credits': 30,
    }
    lesson1_data = {
        'code': 'B1',
        'name': 'Introduction to Music',
        'abstract': 'A summary of what we cover',
    }
    att1_data = {
        'name': 'Reading List',
        'desc': 'Useful stuff you might need',
        'seq': 3,
        'attachment': 'empty_attachment_test.txt',
    }
    att2_data = {
        'name': 'Grammar Guide',
        'desc': 'How do you even spell grammer?',
        'seq': 2,
        'attachment': 'empty_attachment_test.txt',
    }

    def setUp(self):
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.course1 = Course(**self.course1_data)
        self.course1.instructor = self.user1
        self.course1.organiser = self.user1
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        #att1 attached to course
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att1.save()      
        #att2 attached to lesson
        self.att2 = Attachment(lesson=self.lesson1, **self.att1_data)
        self.att2.save()      
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        
    def test_checkrep(self):
        """Test the internal representation checker with attachments"""
        self.assert_(self.uc._checkrep(), "New attachment checkrep failed")
                              
    def test___str__(self):
        """Test that the desired info is in the __str__ method"""
        
        s = self.att1.__str__()
        target = u"Attachment %s, '%s...'" % (self.att1.pk, self.att1.name[:10]) 
        self.assertEqual(s, target, "Incorrect __str__ return")

    def test___unicode__(self):
        """Test that the desired info is in the unicode method"""
        unicod = self.att1.__unicode__()
        target = u"Att. ID:%s, '%s...'" % (self.att1.pk, self.att1.name[:10])  
        self.assertEqual(unicod, target, "Incorrect __unicode__ return")

    def test_get_absolute_url(self):
        """Test the correct url is returned"""
        
        url = self.att1.get_absolute_url()
        target = self.att1.attachment
        self.assertEqual(target.url, url, "attachment URL error")
        
    def test_get_metadata_url(self):
        """Test that the correct metadata url is returned"""
        
        url = self.att1.get_metadata_url()
        target = u"/attachment/%s/metadata/" % self.att1.pk
        self.assertEqual(target, url, "attachment metadata URL error")
