from django.contrib import admin
from .models import Company, Job, Application


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "website")
    search_fields = ("name", "website", "description")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "location", "salary_range", "posted_at")
    search_fields = ("title", "description", "location", "company__name")
    list_filter = ("company", "location", "posted_at")
    list_select_related = ("company",)
    ordering = ("-posted_at",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "applicant", "submitted_at", "resume_link")
    search_fields = (
        "job__title",
        "job__company__name",
        "applicant__username",
        "cover_letter",
    )
    list_filter = ("submitted_at", "job__company")
    list_select_related = ("job", "applicant", "job__company")
    ordering = ("-submitted_at",)
