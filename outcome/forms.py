# outcome/forms.py
from django import forms
from outcome.models import LearningIntention

class LearningIntentionForm(forms.ModelForm):
    class Meta:
        model = LearningIntention

    def __init__(self, *args, **kwargs):
        super(LearningIntentionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['id'] = 'id_learning_intention_text'
        self.fields['text'].widget.attrs['size'] = '40'
