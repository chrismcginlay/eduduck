#outcome/tests/test_forms.py
from django.test import TestCase

from ..forms import (
    LearningIntentionForm,
    LOForm,
    SCForm
)

class LearningIntentionFormTest(TestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome.json',
    ]
    
    def test_form_has_correct_field_ids(self):
        """ Correct id attributes for widgets are rendered """

        form = LearningIntentionForm()
        self.assertEqual(
            form.fields['text'].widget.attrs['id'],
            'id_learning_intention_text'
        )
        self.assertEqual(form.fields['text'].widget.attrs['size'], '40')

    def test_form_renders_correct_fields(self):
        form = LearningIntentionForm()
        self.assertIn('id_learning_intention_text', form.as_p())
        self.assertIn('size="40"', form.as_p())

class SCFormTest(TestCase):

    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome.json',
    ]

    def test_form_has_correct_field_ids(self):
        form = SCForm()
        self.assertEqual(
            form.fields['text'].widget.attrs['id'],
            'id_success_criterion_text'
        )

    def test_form_renders_correct_fields(self):
        form = SCForm()
        self.assertIn('id_success_criterion_text', form.as_p())
        self.assertIn('size="40"', form.as_p())


class LOFormTest(TestCase):

    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome.json',
    ]

    def test_form_has_correct_field_ids(self):
        form = LOForm()
        self.assertEqual(
            form.fields['text'].widget.attrs['id'],
            'id_learning_outcome_text'
        )

    def test_form_renders_correct_fields(self):
        form = LOForm()
        self.assertIn('id_learning_outcome_text', form.as_p())
        self.assertIn('size="40"', form.as_p())


