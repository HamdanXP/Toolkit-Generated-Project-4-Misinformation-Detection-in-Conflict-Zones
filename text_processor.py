import re
import spacy
from langdetect import detect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging

class TextProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            self.logger.error(f'Error initializing NLP components: {e}')
            raise

    def process(self, text):
        """Process input text through cleaning and feature extraction"""
        try:
            # Basic cleaning
            text = self.clean_text(text)
            
            # Language detection
            lang = self.detect_language(text)
            if lang != 'en':
                self.logger.warning(f'Non-English text detected: {lang}')
            
            # Extract features
            features = {
                'cleaned_text': text,
                'urls': self.extract_urls(text),
                'entities': self.extract_entities(text),
                'linguistic_features': self.extract_linguistic_features(text)
            }
            
            return features
            
        except Exception as e:
            self.logger.error(f'Error processing text: {e}')
            raise

    def clean_text(self, text):
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(word for word in text.split() if word not in self.stop_words)
        return text

    def detect_language(self, text):
        """Detect text language"""
        try:
            return detect(text)
        except:
            return 'unknown'

    def extract_urls(self, text):
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)

    def extract_entities(self, text):
        """Extract named entities"""
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def extract_linguistic_features(self, text):
        """Extract linguistic features for analysis"""
        features = {
            'word_count': len(text.split()),
            'avg_word_length': sum(len(word) for word in text.split()) / len(text.split()) if text else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?')
        }
        return features

    def get_risk_factors(self, processed_text):
        """Identify specific risk factors in processed text"""
        risk_factors = []
        
        # Check for warning signs
        if processed_text['linguistic_features']['exclamation_count'] > 3:
            risk_factors.append('Excessive use of exclamation marks')
            
        if len(processed_text['urls']) == 0:
            risk_factors.append('No source citations')
            
        if processed_text['linguistic_features']['word_count'] < 10:
            risk_factors.append('Very short message')
            
        return risk_factors