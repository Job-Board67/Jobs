from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (job_list, job_detail,
    api_jobs, api_job_detail,
    register_view, profile_view)
from . import views

urlpatterns = [
    path("", job_list, name="job_list"),
    path("job/<int:job_id>/", job_detail, name="job_detail"),

    path("api/jobs/", api_jobs, name="api_jobs"),
    path("api/jobs/<int:job_id>/", api_job_detail, name="api_job_detail"),

    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
]