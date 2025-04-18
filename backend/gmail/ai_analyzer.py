import spacy
from typing import Dict, Any

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def analyze_resume(self, text: str) -> Dict[str, Any]:
        doc = self.nlp(text)
        
        return {
            'skills': self._extract_skills(doc),
            'experience': self._extract_experience(doc),
            'education': self._extract_education(doc),
            'score': self._calculate_score(doc),
            'feedback': self._generate_feedback(doc)
        }
    