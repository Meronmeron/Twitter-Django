from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}), 
        }
