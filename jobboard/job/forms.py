from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application

from .models import Profile


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, initial=Profile.STUDENT)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume_link"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write a short cover letter..."
            }),
            "resume_link": forms.URLInput(attrs={
                "placeholder": "Link to your resume"
            }),
        }
