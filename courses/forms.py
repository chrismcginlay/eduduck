# Course forms
from django import forms
from courses.models import Course

class CourseNameForm(forms.Form):
    """ A brief form, just course name and submit """
    course_short_name = forms.CharField(
        widget = forms.fields.TextInput(attrs={
            'placeholder': 'A short name for the course',
            'id': 'id_course_create',
        }),
    )

class CourseFullForm(forms.models.ModelForm):
    """ A fully featured form to create courses """
    class Meta:
        model = Course
        fields = ('code', 'name', 'abstract')
    