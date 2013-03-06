from django import forms

from .models import UserCourse

class SignUpForm(forms.ModelForm):
    """Buttons for user to sign up to course"""
    
    class Meta:
        model = UserCourse
        
