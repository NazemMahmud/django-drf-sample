from django import forms
from .models import Tweet

MAX_LENGTH = 235

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("Tweet is too long...")
        return content
