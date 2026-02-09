from django.urls import path
from django.contrib.auth import views as auth_views
from .views import job_list, job_detail, api_jobs, api_job_detail, register, register_view
from . import views

urlpatterns = [
    path("", job_list, name="job_list"),
    path("<int:job_id>/", job_detail, name="job_detail"),
    path("api/jobs/", api_jobs, name="api_jobs"),
    path("api/jobs/<int:job_id>/", api_job_detail),
    path("profile/", views.profile, name="profile"),
    path("register/", register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", register_view, name="register"),
]
