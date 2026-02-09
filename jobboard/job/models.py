from django.db import models

from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Job(models.Model):
    # Field types: CharField for titles, TextField for descriptions
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    
    # Relationship: A Company can have many Jobs (Many-to-One)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class Application(models.Model):
    # Relationship: A Job can have many Applications
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    # Relationship: A User (applicant) can submit many Applications
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_link = models.URLField()
    cover_letter = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ("EMPLOYER", "Employer"),
        ("STUDENT", "Student"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"