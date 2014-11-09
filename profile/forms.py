from django import forms

from .models import Profile 

class ProfileEditForm(forms.ModelForm):
    """Facilities for user to edit profile data"""
    
    class Meta:
        model = Profile
        exclude = ('user', )
    
    
