from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Job, Profile, Company

CREATE_NEW_COMPANY_VALUE = "__new__"

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


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

class JobCreateForm(forms.ModelForm):
    company = forms.ChoiceField(label="Company")
    new_company_name = forms.CharField(label="New company name", required=False)

    class Meta:
        model = Job
        fields = ["title", "company", "location", "salary_range", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        companies = Company.objects.order_by("name")
        choices = [(str(c.id), c.name) for c in companies]
        choices.insert(0, (CREATE_NEW_COMPANY_VALUE, "+ Create new company"))
        self.fields["company"].choices = choices

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("company") == CREATE_NEW_COMPANY_VALUE and not cleaned.get("new_company_name"):
            self.add_error("new_company_name", "Enter company name.")
        return cleaned