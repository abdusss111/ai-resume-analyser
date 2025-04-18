from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPost(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.JSONField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.ForeignKey('email_app.CV', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    match_score = models.FloatField(default=0.0)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job', 'applicant') 