import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Company
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def job_list(request):
    jobs = Job.objects.select_related("company").all()
    return render(request, "job_list.html", {"jobs": jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "job_detail.html", {"job": job})
def is_employer(user):
    return hasattr(user, "profile") and user.profile.role == "EMPLOYER"

@login_required
def create_job(request):
    if not is_employer(request.user):
        return HttpResponseForbidden("Only Employers can create jobs.")

@csrf_exempt
def api_jobs(request):
    # GET: list
    if request.method == "GET":
        jobs = Job.objects.select_related("company").values(
            "id",
            "title",
            "location",
            "salary_range",
            "company__name"
        )
        return JsonResponse(list(jobs), safe=False)

    # POST: create
    if request.method == "POST":
        data = json.loads(request.body or "{}")

        job = Job.objects.create(
            title=data.get("title", ""),
            description=data.get("description", ""),
            location=data.get("location", ""),
            salary_range=data.get("salary_range", ""),
            company=Company.objects.get(id=data.get("company_id"))
        )

        return JsonResponse({"created": True, "id": job.id})

    return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def api_job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # GET
    if request.method == "GET":
        return JsonResponse({
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "salary_range": job.salary_range
        })

    # PUT
    if request.method == "PUT":
        data = json.loads(request.body or "{}")
        job.title = data.get("title", job.title)
        job.location = data.get("location", job.location)
        job.salary_range = data.get("salary_range", job.salary_range)
        job.save()
        return JsonResponse({"updated": True})

    # DELETE
    if request.method == "DELETE":
        job.delete()
        return JsonResponse({"deleted": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)
