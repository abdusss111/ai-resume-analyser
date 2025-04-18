
from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'filename', 'uploaded_at', 'content', 'parsed_data']
        read_only_fields = ['id', 'uploaded_at']
