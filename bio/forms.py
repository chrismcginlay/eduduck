from django import forms

from .models import Bio

class BioEditForm(forms.ModelForm):
    """Facilities for user to edit bio data"""
    
    class Meta:
        model = Bio
        exclude = ('user', )
    
    