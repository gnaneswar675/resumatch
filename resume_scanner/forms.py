from django import forms
from .models import Applicant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'resume', 'job']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
        }

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ResumeFraudForm(forms.Form):
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
