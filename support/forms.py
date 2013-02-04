from django import forms

class SupportForm(forms.Form):
    """General request for support or contact"""
    subject = forms.CharField(max_length = 100)
    email = forms.EmailField(label='Your email')
    message = forms.CharField(widget = forms.Textarea)
    
    def clean_message(self):
        """Sensible messages cannot be too short"""
        
        message = self.cleaned_data['message']
        wc = len(message.split())
        if wc < 4:
            raise forms.ValidationError(
                "Please muster four or more words of wisdom or woe!"
            )
        return message
    
    