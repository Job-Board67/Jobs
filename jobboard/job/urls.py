from django.urls import path
from .views import job_list, job_detail, api_jobs

urlpatterns = [
    path("", job_list, name="job_list"),
    path("<int:job_id>/", job_detail, name="job_detail"),
    path("api/jobs/", api_jobs, name="api_jobs"),
]
