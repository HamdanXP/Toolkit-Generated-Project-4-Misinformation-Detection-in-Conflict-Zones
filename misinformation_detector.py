import tkinter as tk
from tkinter import ttk, scrolledtext
from text_processor import TextProcessor
from model_trainer import ModelPredictor
from credibility_scorer import CredibilityScorer
from gui_interface import MisinformationGUI
import yaml
import logging

class MisinformationDetector:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Load configuration
        try:
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f'Error loading config: {e}')
            raise

        # Initialize components
        self.text_processor = TextProcessor()
        self.model_predictor = ModelPredictor()
        self.credibility_scorer = CredibilityScorer()
        
    def analyze_text(self, text, source_url=None):
        """Analyze text for potential misinformation"""
        try:
            # Process text
            processed_text = self.text_processor.process(text)
            
            # Get model prediction
            risk_score = self.model_predictor.predict(processed_text)
            
            # Check source credibility if URL provided
            cred_score = None
            if source_url:
                cred_score = self.credibility_scorer.score_url(source_url)
            
            # Generate explanation
            explanation = self.generate_explanation(risk_score, processed_text, cred_score)
            
            return {
                'risk_score': risk_score,
                'credibility_score': cred_score,
                'explanation': explanation
            }
            
        except Exception as e:
            self.logger.error(f'Error analyzing text: {e}')
            raise

    def generate_explanation(self, risk_score, processed_text, cred_score):
        """Generate human-readable explanation of results"""
        explanation = []
        
        if risk_score > 0.7:
            explanation.append('High risk of misinformation detected')
        elif risk_score > 0.4:
            explanation.append('Moderate risk of misinformation detected')
        else:
            explanation.append('Low risk of misinformation detected')
            
        # Add specific risk factors
        risk_factors = self.text_processor.get_risk_factors(processed_text)
        for factor in risk_factors:
            explanation.append(f'- {factor}')
            
        if cred_score is not None:
            explanation.append(f'Source credibility score: {cred_score}')
            
        return explanation

def main():
    detector = MisinformationDetector()
    gui = MisinformationGUI(detector)
    gui.run()

if __name__ == '__main__':
    main()