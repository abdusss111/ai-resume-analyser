from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import JobPost, JobApplication
from .serializers import JobPostSerializer, JobApplicationSerializer
from email_app.models import CV

class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'location']

    def get_queryset(self):
        if self.request.user.role == 'recruiter':
            return JobPost.objects.filter(recruiter=self.request.user)
        return JobPost.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'recruiter':
            return JobApplication.objects.filter(job__recruiter=self.request.user)
        return JobApplication.objects.filter(applicant=self.request.user)

    @action(detail=False, methods=['post'])
    def apply(self, request):
        job_id = request.data.get('job_id')
        cv_id = request.data.get('cv_id')

        try:
            job = JobPost.objects.get(id=job_id)
            cv = CV.objects.get(id=cv_id, user=request.user)

            # Проверяем, не подавал ли уже пользователь заявку
            if JobApplication.objects.filter(job=job, applicant=request.user).exists():
                return Response(
                    {'error': 'You have already applied for this job'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем заявку
            application = JobApplication.objects.create(
                job=job,
                applicant=request.user,
                cv=cv
            )

            # Запускаем процесс matching
            from .tasks import calculate_match_score
            calculate_match_score.delay(application.id)

            return Response(
                JobApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )

        except (JobPost.DoesNotExist, CV.DoesNotExist):
            return Response(
                {'error': 'Invalid job or CV ID'},
                status=status.HTTP_400_BAD_REQUEST
            ) 