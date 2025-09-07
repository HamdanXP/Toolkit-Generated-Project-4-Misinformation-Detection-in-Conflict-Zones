import re
import requests
from urllib.parse import urlparse
import logging

class CredibilityScorer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.known_reliable_domains = [
            'who.int',
            'un.org',
            'reliefweb.int',
            'icrc.org'
        ]

    def score_url(self, url):
        """Score credibility of source URL"""
        try:
            # Basic URL validation
            if not self.is_valid_url(url):
                return 0.0
                
            # Parse domain
            domain = urlparse(url).netloc
            
            # Check against known reliable sources
            if domain in self.known_reliable_domains:
                return 1.0
                
            # Basic checks
            score = 0.5  # Start with neutral score
            
            # Check HTTPS
            if url.startswith('https'):
                score += 0.1
                
            # Check domain age and reputation
            # This would require external API integration
            
            return score
            
        except Exception as e:
            self.logger.error(f'Error scoring URL: {e}')
            return 0.0

    def is_valid_url(self, url):
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False