import google.generativeai as genai
from typing import Optional
from utils.config import env


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
        self._model = genai.GenerativeModel('gemini-2.5-flash')
    
    @property
    def model(self):
        """Get the Gemini model instance"""
        return self._model
    
    def generate_content(self, prompt: str, **kwargs):
        return self._model.generate_content(prompt, **kwargs)
    
    def get_model(self, model_name: str = 'gemini-2.5-flash'):
        return genai.GenerativeModel(model_name)
# Create and export singleton instance (similar to Node.js default export)
gemini_ai = GeminiAI()
