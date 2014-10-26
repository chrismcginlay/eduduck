#attachment/forms.py

from attachment.models import Attachment
from django import forms

ATTACHMENT_NAME_FIELD_REQUIRED_ERROR = "Please supply a name for the " \
    "attachment."
ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR = "You haven't specified a file " \
    "to attach!"

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        error_messages = {
            'name':{'required':ATTACHMENT_NAME_FIELD_REQUIRED_ERROR},
            'attachment':{
                'required':ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR,
            }
        }     

    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['id'] = \
            'id_attachment_title'
        self.fields['attachment'].widget.attrs['id'] = \
             'id_attachment_attachment'

