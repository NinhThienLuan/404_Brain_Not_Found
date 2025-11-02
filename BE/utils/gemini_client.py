import google.generativeai as genai
from typing import Optional
from BE.utils.config import env


class GeminiAI:
    """Gemini AI client singleton - similar to Node.js export pattern"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiAI, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Gemini AI with API key from environment"""
        if not env.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Configure Gemini API
        genai.configure(api_key=env.GEMINI_API_KEY)
        
        # Create default model
        self._model = genai.GenerativeModel('gemini-pro')
    
    @property
    def model(self):
        """Get the Gemini model instance"""
        return self._model
    
    def generate_content(self, prompt: str, **kwargs):
        """
        Generate content using Gemini
        
        Args:
            prompt: The prompt text
            **kwargs: Additional arguments for generate_content
            
        Returns:
            Generated content response
        """
        return self._model.generate_content(prompt, **kwargs)
    
    def get_model(self, model_name: str = 'gemini-pro'):
        """
        Get a specific Gemini model
        
        Args:
            model_name: Name of the model to use
            
        Returns:
            GenerativeModel instance
        """
        return genai.GenerativeModel(model_name)


# Create and export singleton instance (similar to Node.js default export)
gemini_ai = GeminiAI()
