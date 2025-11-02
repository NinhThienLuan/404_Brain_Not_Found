from typing import Optional
from BE.utils.gemini_client import gemini_ai
from BE.utils.config import env


class GeminiRepository:
    """Repository for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API client using singleton"""
        self.gemini_client = gemini_ai
        self.model = self.gemini_client.model
    
    def generate_code(self, prompt: str, model_name: str = "gemini-2.5-flash") -> str:
        try:
            # Get specific model if requested or use default
            if model_name:
                model = self.gemini_client.get_model(model_name)
            else:
                model = self.model
            
            response = model.generate_content(prompt)
            
            # Check if response has text
            if not response or not hasattr(response, 'text'):
                raise Exception("No response received from Gemini")
            
            if not response.text:
                raise Exception("Empty response from Gemini")
            
            return response.text
        except Exception as e:
            raise Exception(f"Error generating code: {str(e)}")
    
    def review_code(self, code: str, language: str, review_type: str = "general", model_name: str = "gemini-2.5-flash") -> str:

        try:
            prompt = f"""
            Please review the following {language} code with focus on {review_type} aspects:
            
            ```{language}
            {code}
            ```
            
            Provide:
            1. Overall score (0-10)
            2. List of issues with severity (critical, high, medium, low, info)
            3. Specific suggestions for improvements
            4. Summary of code quality
            """
            
            # Get specific model if requested
            model = self.gemini_client.get_model(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error reviewing code: {str(e)}")
    
    def chat(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in chat: {str(e)}")
