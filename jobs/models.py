from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # ek user ek job par ek hi baar apply kare

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"
