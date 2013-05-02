from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from interaction.models import UserCourse, UserAttachment

from ..models import Attachment

class AttachmentViewTests(TestCase):
    """Test views for user interaction with attachments"""

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
    att1_data = {'att_code': 'DOC1',
                        'att_name': 'Reading List',
                        'att_desc': 'Useful stuff you might need',
                        'att_seq': 3,
                        'attachment': 'empty_attachment_test.txt',
                        }
    att2_data = {'att_code': 'DOC2',
                        'att_name': 'Grammer Guide',
                        'att_desc': 'How do you even spell grammer?',
                        'att_seq': 2,
                        'attachment': 'empty_attachment_test.txt',
                        }

    def setUp(self):
        self.course1 = Course(**self.course1_data)
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        
        self.user1 = User.objects.create_user('bertie', 'bertie@example.com', 
                                              'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.uc = UserCourse(course=self.course1, user=self.user1)
        self.uc.save()
        
        self.att1 = Attachment(course=self.course1, **self.att1_data)
        self.att2 = Attachment(lesson=self.lesson1, **self.att2_data)
        self.att1.save()
        self.att2.save()        
        
    def test_view_metadata(self):
        """Verify that the relevant metadata get rendered"""

        import pdb; pdb.set_trace()        
        response = self.client.get(self.att1.get_metadata_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['attachment'])
        self.assertIn("Reading List", response.content, 
                      "detail missing from response")