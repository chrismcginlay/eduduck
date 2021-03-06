from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course
from lesson.models import Lesson
from interaction.models import UserCourse, UserAttachment

from ..models import Attachment

class AttachmentViewTests(TestCase):
    """Test views for user interaction with attachments"""

    course1_data = {
        'code': 'EDU02',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
    }
    lesson1_data = {
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
        self.user1 = User.objects.create_user(
            'bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('dave', 'dave@dave.com', 'dave')
        self.user2.is_active = True
        self.user2.save()
        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        
        self.uc = UserCourse(course=self.course1, user=self.user2)
        self.uc.save()
        
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att2 = Attachment(lesson=self.lesson1, **self.att2_data)
        self.att1.save()
        self.att2.save()        
        
    def test_view_metadata(self):
        """Verify that the relevant metadata get rendered"""

        response = self.client.get(self.att1.get_metadata_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['attachment'])
        self.assertIn("Reading List", response.content, 
                      u"detail missing from response")

