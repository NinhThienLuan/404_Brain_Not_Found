from typing import Optional
from utils.gemini_client import gemini_ai
from utils.config import env


class GeminiRepository:
    """Repository for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API client using singleton"""
        self.gemini_client = gemini_ai
        self.model = self.gemini_client.model
    
    def generate_code(self, prompt: str) -> str:
        """
        Generate code using Gemini API
        
        Args:
            prompt: The prompt for code generation
            
        Returns:
            Generated code as string
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating code: {str(e)}")
    
    def review_code(self, code: str, language: str, review_type: str = "general") -> str:
        """
        Review code using Gemini API
        
        Args:
            code: The code to review
            language: Programming language
            review_type: Type of review (general, security, performance, style)
            
        Returns:
            Review result as string
        """
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
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error reviewing code: {str(e)}")
    
    def chat(self, prompt: str) -> str:
        """
        General chat with Gemini API
        
        Args:
            prompt: The prompt/question
            
        Returns:
            Response as string
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error in chat: {str(e)}")
