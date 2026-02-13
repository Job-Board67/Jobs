from django import forms
from .models import Job, Company

CREATE_NEW_COMPANY_VALUE = "__new__"

class JobCreateForm(forms.ModelForm):
    company_choice = forms.ChoiceField(label="Company")
    new_company_name = forms.CharField(
        label="New company name",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Only if you choose + Create new company"})
    )

    class Meta:
        model = Job
        # ВАЖНО: company тут НЕТ
        fields = ["title", "location", "salary_range", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        companies = Company.objects.order_by("name")
        choices = [(str(c.id), c.name) for c in companies]
        choices.insert(0, (CREATE_NEW_COMPANY_VALUE, "+ Create new company"))
        self.fields["company_choice"].choices = choices

    def clean(self):
        cleaned = super().clean()
        choice = cleaned.get("company_choice")
        new_name = (cleaned.get("new_company_name") or "").strip()

        if choice == CREATE_NEW_COMPANY_VALUE and not new_name:
            self.add_error("new_company_name", "Enter company name.")
        return cleaned

    def save(self, commit=True):
        job = super().save(commit=False)

        choice = self.cleaned_data["company_choice"]
        new_name = (self.cleaned_data.get("new_company_name") or "").strip()

        if choice == CREATE_NEW_COMPANY_VALUE:
            company, _ = Company.objects.get_or_create(name=new_name)
        else:
            company = Company.objects.get(pk=int(choice))

        job.company = company  # ✅ вот тут FK получает Company instance

        if commit:
            job.save()
        return job
