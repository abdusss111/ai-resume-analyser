from celery import shared_task
from .models import JobApplication
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@shared_task
def calculate_match_score(application_id):
    try:
        application = JobApplication.objects.get(id=application_id)
        
        nlp = spacy.load('en_core_web_lg')
        
        cv_text = application.cv.get_text_content()  
        job_description = application.job.description
        
        vectorizer = TfidfVectorizer(stop_words='english')
        
        vectors = vectorizer.fit_transform([cv_text, job_description])
        
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        application.match_score = similarity * 100 
        application.save()
        
        return True
        
    except Exception as e:
        print(f"Error calculating match score: {e}")
        return False 