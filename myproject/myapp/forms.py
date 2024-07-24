from django import forms
from .models import Job, Candidate

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'resume']
