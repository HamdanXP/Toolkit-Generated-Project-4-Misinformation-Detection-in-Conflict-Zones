from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import logging

class ModelPredictor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            # Load trained model and vectorizer
            with open('models/classifier.pkl', 'rb') as f:
                self.classifier = pickle.load(f)
            with open('models/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
        except Exception as e:
            self.logger.error(f'Error loading model: {e}')
            raise

    def predict(self, processed_text):
        """Generate risk score for processed text"""
        try:
            # Vectorize text
            text_features = self.vectorizer.transform([processed_text['cleaned_text']])
            
            # Get prediction probability
            risk_score = self.classifier.predict_proba(text_features)[0][1]
            
            # Adjust score based on linguistic features
            risk_score = self.adjust_score(risk_score, processed_text)
            
            return risk_score
            
        except Exception as e:
            self.logger.error(f'Error making prediction: {e}')
            raise

    def adjust_score(self, base_score, processed_text):
        """Adjust risk score based on additional features"""
        features = processed_text['linguistic_features']
        
        # Increase risk for very short or very long texts
        if features['word_count'] < 10 or features['word_count'] > 500:
            base_score *= 1.2
            
        # Increase risk for excessive punctuation
        if features['exclamation_count'] > 3:
            base_score *= 1.1
            
        # Cap score at 1.0
        return min(base_score, 1.0)