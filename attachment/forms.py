#attachment/forms.py
from django import forms
from .models import Attachment

class AttachmentUploadForm(forms.ModelForm):
    class Meta:
        model = Attachment
        
        