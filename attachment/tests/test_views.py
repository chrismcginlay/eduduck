from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from interaction.models import UserCourse, UserAttachment

class AttachmentViewTests(TestCase):
    """Test views for user interaction with attachments"""

    course1_data = {'course_code': 'EDU02',
                   'course_name': 'A Course of Leeches',
                   'course_abstract': 'Learn practical benefits of leeches',
                   'course_organiser': 'Van Gogh',
                   'course_level': 'Basic',
                   'course_credits': 30,
                   }
    lesson1_data = {}
    attachment1_data = {}
    attachment2_data= {}

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
        
        
    def test_view_metadata(self):
        """Verify that the relevant metadata get rendered"""
        
        self.fail