#attachment/test/test_forms.py
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..forms import (
    ATTACHMENT_NAME_FIELD_REQUIRED_ERROR,
    ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR, 
    AttachmentForm
)
from ..utils import generate_file

class AttachmentFormTest(TestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'videos.json',
    ]
    
    def test_form_has_correct_field_ids(self):
        """ Correct id attributes for widgets are rendered """

        form = AttachmentForm()
        self.assertEqual(
            form.fields['name'].widget.attrs['id'], 'id_attachment_title')

    def test_form_renders_correct_fields(self):
        form = AttachmentForm()
        self.assertIn('id_attachment_title', form.as_p())
        self.assertIn('id_attachment_attachment', form.as_p())

    def test_form_has_correct_error_messages(self):
        # Missing required fields
        form = AttachmentForm(
            data={'course':u'1', 'name':'', 'attachment':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [ATTACHMENT_NAME_FIELD_REQUIRED_ERROR],
            'attachment': [ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)

    def test_form_create_new_course_attachment(self):
        #http://stackoverflow.com/a/20508664        
        data = {
            'course':u'1',
            'name':'Attachment test',
        }
        file_data = {'attachment': SimpleUploadedFile('testfile.txt', 'A test file') }
        form = AttachmentForm(data, file_data)
        self.assertTrue(form.is_valid())
        form.save()
