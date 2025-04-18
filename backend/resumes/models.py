

from django.db import models

class Resume(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  
    parsed_data = models.JSONField(default=dict) 

    def __str__(self):
        return f"Resume of {self.user.email} - {self.filename}"
