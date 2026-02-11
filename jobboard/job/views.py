import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Company, Application
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import ApplicationForm, RegisterForm
from .models import Profile


@login_required
def job_list(request):
    jobs = Job.objects.select_related("company").order_by("-posted_at")
    return render(request, "job_list.html", {"jobs": jobs})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists()

    return render(request, "job_detail.html", {
        "job": job,
        "already_applied": already_applied,
    })

def is_employer(user):
    return hasattr(user, "profile") and user.profile.role == "EMPLOYER"

def register_view(request):
    if request.user.is_authenticated:
        return redirect("job_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data["role"]
            Profile.objects.update_or_create(user=user, defaults={"role": role})

            login(request, user)
            return redirect("job_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def employer_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.profile.role != Profile.Role.EMPLOYER:
            return render(request, "forbidden.html", status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped
@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # ❗ защита от повторного отклика
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect("job_detail", job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, "apply.html", {
        "job": job,
        "form": form
    })

@employer_required
def create_job(request):
    if not is_employer(request.user):
        return HttpResponseForbidden("Only Employers can create jobs.")

@login_required
def profile_view(request):
    return render(request, "profile.html", {"profile": request.user.profile})
@login_required
def api_jobs(request):
    jobs = Job.objects.select_related("company").order_by("-posted_at")
    data = [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company.name,
            "location": j.location,
            "salary_range": j.salary_range,
        }
        for j in jobs
    ]
    return JsonResponse(data, safe=False)

@login_required
def api_job_detail(request, job_id):
    j = get_object_or_404(Job.objects.select_related("company"), id=job_id)
    data = {
        "id": j.id,
        "title": j.title,
        "company": j.company.name,
        "location": j.location,
        "salary_range": j.salary_range,
        "description": j.description,
    }
    return JsonResponse(data)