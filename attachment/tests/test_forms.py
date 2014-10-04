#attachment/test/test_forms.py
from django.test import TestCase

from ..forms import (
    ATTACHMENT_NAME_FIELD_REQUIRED_ERROR,
    ATTACHEMENT_URI_FIELD_REQUIRED_ERROR,
    AttachmentForm
)

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
        form = VideoForm()
        self.assertIn('id_attachment_title', form.as_p())
        self.assertIn('id_attachment_uri', form.as_p())

    def test_form_has_correct_error_messages(self):
        # Missing required fields
        form = AttachmentForm(
            data={'course':u'1', 'name':'', 'uri':''})
        self.assertFalse(form.is_valid())
        expected_errors = {
            'name': [ABSTRACT_NAME_FIELD_REQUIRED_ERROR],
            'url': [ABSTRACT_URI_FIELD_REQUIRED_ERROR]
        }
        self.assertEqual(form.errors, expected_errors)

