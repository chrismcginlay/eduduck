# video/forms.py
from django import forms
from video.models import Video

VIDEO_URL_FIELD_INVALID_ERROR = "Please check your video URL," \
    " it seem's invalid."
VIDEO_NAME_FIELD_REQUIRED_ERROR = "Please provide a descriptive name" \
    " for the video."
VIDEO_URL_FIELD_REQUIRED_ERROR = "Please provide a url for the video."

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        error_messages = {
            'name':{'required':VIDEO_NAME_FIELD_REQUIRED_ERROR},
            'url':{
                'required':VIDEO_URL_FIELD_REQUIRED_ERROR,
                'invalid':VIDEO_URL_FIELD_INVALID_ERROR}
        }     

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['id'] = 'id_video_title'
        self.fields['url'].widget.attrs['url'] = 'id_video_url'
