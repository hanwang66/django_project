from django import forms
from .models import EnglishStudyRecord

class EnglishStudyRecordForm(forms.ModelForm):
    class Meta:
        model = EnglishStudyRecord
        fields = ['title', 'content', 'duration', 'tips']