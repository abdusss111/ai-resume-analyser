import spacy
import pytesseract
from pdf2image import convert_from_path
import docx2txt
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.skill_patterns = self._load_skill_patterns()

    def _load_skill_patterns(self):
        return ["python", "java", "javascript", "sql", "react", "vue", "django"]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            images = convert_from_path(pdf_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_path: str) -> str:
        try:
            return docx2txt.process(docx_path)
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""

    def analyze_resume(self, file_path: str) -> Dict[str, Any]:
        # Определяем тип файла и извлекаем текст
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        doc = self.nlp(text)
        
        analysis = {
            'skills': self._extract_skills(doc),
            'experience': self._extract_experience(doc),
            'education': self._extract_education(doc),
            'contact_info': self._extract_contact_info(doc),
            'score': self._calculate_score(doc),
            'feedback': self._generate_feedback(doc)
        }
        
        return analysis

    def _extract_skills(self, doc):
        skills = []
        for token in doc:
            if token.text.lower() in self.skill_patterns:
                skills.append(token.text)
        return list(set(skills))

    def _extract_experience(self, doc):
        experience = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'DATE']:
                experience.append({
                    'entity': ent.text,
                    'type': ent.label_
                })
        return experience

    def _extract_education(self, doc):
        education = []
        education_keywords = ['university', 'college', 'school', 'bachelor', 'master', 'phd']
        
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in education_keywords):
                education.append(sent.text.strip())
        
        return education

    def _calculate_score(self, doc):
        score = 0
        skills_found = len(self._extract_skills(doc))
        experience_found = len(self._extract_experience(doc))
        education_found = len(self._extract_education(doc))
        
        score += skills_found * 0.4
        score += experience_found * 0.4
        score += education_found * 0.2
        
        return min(score, 10.0)  

    def _generate_feedback(self, doc):
        feedback = {
            'improvements': [],
            'strengths': [],
            'missing_sections': []
        }
        
        sections = {
            'contact': False,
            'education': False,
            'experience': False,
            'skills': False
        }
        
        skills = self._extract_skills(doc)
        if len(skills) < 5:
            feedback['improvements'].append("Consider adding more specific skills to your resume")
        else:
            feedback['strengths'].append("Good variety of skills listed")
            
        return feedback 