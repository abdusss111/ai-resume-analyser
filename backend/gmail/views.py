from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from rest_framework import generics, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend
from .models import CV
from .serializers import CVSerializer, CVDetailSerializer
from .ai_analyzer import ResumeAnalyzer
from celery import shared_task
from .tasks import analyze_resume
from django.core.cache import cache


@shared_task
def process_resume(cv_id):
    cv = CV.objects.get(id=cv_id)
    analyzer = ResumeAnalyzer()
    
    try:
        # Чтение файла резюме
        with default_storage.open(cv.resume_file.name, 'r') as file:
            content = file.read()
        
        # Анализ резюме
        analysis_results = analyzer.analyze_resume(content)
        
        # Обновление модели CV результатами анализа
        cv.skills = analysis_results['skills']
        cv.experience = analysis_results['experience']
        cv.education = analysis_results['education']
        cv.ai_score = analysis_results['score']
        cv.ai_feedback = analysis_results['feedback']
        cv.processing_status = 'processed'
        cv.save()
        
    except Exception as e:
        cv.processing_status = 'failed'
        cv.save()
        raise e


class CVViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'skills']
    filterset_fields = ['processing_status', 'ai_score']

    def get_queryset(self):
        if self.request.user.role == 'recruiter':
            return CV.objects.all()
        return CV.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CVDetailSerializer
        return CVSerializer

    def perform_create(self, serializer):
        cv = serializer.save(user=self.request.user)
        analyze_resume.delay(cv.id)

    @action(detail=True, methods=['post'])
    def reanalyze(self, request, pk=None):
        cv = self.get_object()
        analyze_resume.delay(cv.id)
        return Response({'status': 'Analysis started'})

    def list(self, request, *args, **kwargs):
        cache_key = f'cv_list_{request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
            
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)  
        return response


def share_cv_email(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)

    recipient_email = request.POST.get('email')

    if recipient_email:

        subject = f"{cv.name}'s CV"

        message = f"Check out {cv.name}'s CV at {request.build_absolute_uri(cv.profile_picture.url)}"

        sender_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, sender_email, [recipient_email])

        messages.success(request, "CV shared successfully via email.")

    else:

        messages.error(request, "Please provide a valid email.")

    return redirect('cv_list')


def cv_list(request):
    cvs = CV.objects.all()  
    return render(request, 'cv_list.html', {'cvs': cvs}) 