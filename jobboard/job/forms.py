from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, initial=Profile.STUDENT)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")
