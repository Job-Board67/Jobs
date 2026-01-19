import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Company
from django.shortcuts import render, get_object_or_404



def job_list(request):
    jobs = Job.objects.select_related("company").all()
    return render(request, "job_list.html", {"jobs": jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "job_detail.html", {"job": job})

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
