# outcome/forms.py
from django import forms
from outcome.models import (
    LearningIntention,
    LearningIntentionDetail
)

class LearningIntentionForm(forms.ModelForm):
    class Meta:
        model = LearningIntention

    def __init__(self, *args, **kwargs):
        super(LearningIntentionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['id'] = 'id_learning_intention_text'
        self.fields['text'].widget.attrs['size'] = '40'

class SCForm(forms.ModelForm):
    class Meta:
        model = LearningIntentionDetail

class LOFOrm(forms.ModelForm):
    class Meta:
        model = LearningIntentionDetail
