# outcome/forms.py
from django import forms
from outcome.models import (
    LearningIntention,
    LearningIntentionDetail
)

class LearningIntentionForm(forms.ModelForm):
    class Meta:
        model = LearningIntention
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(LearningIntentionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['id'] = 'id_learning_intention_text'
        self.fields['text'].widget.attrs['size'] = '40'

class SCForm(forms.ModelForm):
    class Meta:
        model = LearningIntentionDetail
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super(SCForm, self).__init__(*args, **kwargs)
        self.initial['lid_type'] = u'SC'
        self.fields['text'].widget.attrs['id'] = 'id_success_criterion_text'
        self.fields['text'].widget.attrs['size'] = '40'

class LOForm(forms.ModelForm):
    class Meta:
        model = LearningIntentionDetail
        fields = ['text']
     
    def __init__(self, *args, **kwargs):
        super(LOForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['id'] = 'id_learning_outcome_text'
        self.fields['text'].widget.attrs['size'] = '40'
