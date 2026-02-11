from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    resume_link = models.URLField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} -> {self.job}"


class Profile(models.Model):
    EMPLOYER = "employer"
    STUDENT = "student"

    ROLE_CHOICES = [
        (EMPLOYER, "Employer"),
        (STUDENT, "Student"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    # создаём профиль только один раз, безопасно
    if created:
        Profile.objects.get_or_create(user=instance)
