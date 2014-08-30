# Course forms
from django import forms
from courses.models import Course

COURSE_NAME_FIELD_REQUIRED_ERROR = "A course must have a short title"
COURSE_ABSTRACT_FIELD_REQUIRED_ERROR = "You must provide an abstract"\
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
            'name': {'required': COURSE_NAME_FIELD_REQUIRED_ERROR},
            'abstract': {'required': COURSE_ABSTRACT_FIELD_REQUIRED_ERROR},
        }
