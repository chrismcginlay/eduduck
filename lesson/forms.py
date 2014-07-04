# lessons/forms.py

from django import forms
from lesson.models import Lesson

class LessonEditForm(forms.ModelForm):
    class Meta:
	model = Lesson

    def __init__(self, *args, **kwargs):
        super(LessonEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['id'] = 'id_lesson_title'
