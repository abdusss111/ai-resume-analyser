from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CV(models.Model):
    PROCESSING_STATUS = (
        ('pending', 'В обработке'),
        ('processed', 'Обработано'),
        ('failed', 'Ошибка обработки')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cvs')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='cv_pictures/', blank=True, null=True)
    resume_file = models.FileField(upload_to='cv_resumes/')
    date_created = models.DateTimeField(auto_now_add=True)
    
    skills = models.JSONField(default=dict, blank=True)
    experience = models.JSONField(default=dict, blank=True)
    education = models.JSONField(default=dict, blank=True)
    ai_score = models.FloatField(default=0.0)
    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS,
        default='pending'
    )
    ai_feedback = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name}'s CV"