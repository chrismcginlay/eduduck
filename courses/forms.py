# Course forms
from django import forms
from courses.models import Course

NAME_FIELD_REQUIRED_ERROR = "A course must have a short title"
NAME_FIELD_TOO_LONG_ERROR = "Please ensure the course name is 13 characters"\
    " or fewer"
CODE_FIELD_REQUIRED_ERROR = "Please provide a code for the course"
ABSTRACT_FIELD_REQUIRED_ERROR = "You must provide an abstract"\
    " (brief description)"

class CourseNameForm(forms.Form):
    """ A brief form, just course name and submit """
    course_short_name = forms.CharField(
        widget = forms.fields.TextInput(attrs={
            'placeholder': 'A short name for the course',
            'id': 'id_course_name',
        }),
    )

class CourseFullForm(forms.models.ModelForm):
    """ A fully featured form to create courses """
    class Meta:
        model = Course
        fields = ('code', 'name', 'abstract')
        error_messages = {
            'name': {'required': NAME_FIELD_REQUIRED_ERROR},
            'code': {'required': CODE_FIELD_REQUIRED_ERROR},
            'abstract': {'required': ABSTRACT_FIELD_REQUIRED_ERROR},
        }
