from celery import shared_task
from .models import CV
from .services.ai_analysis import ResumeAnalyzer
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def analyze_resume(self, cv_id):
    try:
        cv = CV.objects.get(id=cv_id)
        analyzer = ResumeAnalyzer()
        
        # Получаем путь к файлу
        file_path = cv.resume_file.path
        
        # Анализируем резюме
        analysis_results = analyzer.analyze_resume(file_path)
        
        # Обновляем модель CV
        cv.skills = analysis_results['skills']
        cv.experience = analysis_results['experience']
        cv.education = analysis_results['education']
        cv.ai_score = analysis_results['score']
        cv.ai_feedback = analysis_results['feedback']
        cv.processing_status = 'processed'
        cv.save()
        
        return True
        
    except Exception as exc:
        logger.error(f"Error processing resume {cv_id}: {exc}")
        cv.processing_status = 'failed'
        cv.save()
        raise self.retry(exc=exc) 