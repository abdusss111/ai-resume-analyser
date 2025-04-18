
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
from .ai.resume_parser import parse_resume  

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file = request.data.get('resume')
        if file is None:
            return Response({'error': 'No resume file provided'}, status=400)

        resume = Resume.objects.create(
            user=request.user,
            filename=file.name,
            content=file.read().decode('utf-8')  
        )

        parsed_data = parse_resume(resume.content)
        resume.parsed_data = parsed_data
        resume.save()

        return Response(ResumeSerializer(resume).data, status=201)
