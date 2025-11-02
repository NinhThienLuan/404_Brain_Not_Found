from datetime import datetime
from typing import Optional
import json
import re

from BE.model.ai_models import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    CodeReviewRequest,
    CodeReviewResponse,
    ReviewIssue
)
from BE.repository.gemini_repo import GeminiRepository


class CodeGenerationService:
    """Service for code generation using AI"""
    
    def __init__(self, gemini_repo: Optional[GeminiRepository] = None):
        """
        Initialize code generation service
        
        Args:
            gemini_repo: Optional GeminiRepository instance
        """
        self.gemini_repo = gemini_repo or GeminiRepository()
    
    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        """
        Generate code based on request
        
        Args:
            request: CodeGenerationRequest object
            
        Returns:
            CodeGenerationResponse object
        """
        try:
            # Build comprehensive prompt
            prompt = self._build_generation_prompt(request)
            
            # Call Gemini API with specified model
            response_text = self.gemini_repo.generate_code(prompt, model_name=request.model)
            
            # Parse response
            generated_code, explanation = self._parse_generation_response(response_text)
            
            return CodeGenerationResponse(
                generated_code=generated_code,
                explanation=explanation,
                language=request.language,
                timestamp=datetime.now(),
                success=True
            )
        except Exception as e:
            return CodeGenerationResponse(
                generated_code="",
                explanation="",
                language=request.language,
                timestamp=datetime.now(),
                success=False,
                error_message=str(e)
            )
    
    def _build_generation_prompt(self, request: CodeGenerationRequest) -> str:
        """Build prompt for code generation"""
        prompt = f"Generate {request.language} code for the following requirement:\n\n"
        prompt += f"{request.prompt}\n\n"
        
        if request.framework:
            prompt += f"Use {request.framework} framework.\n"
        
        if request.additional_context:
            prompt += f"Additional context: {request.additional_context}\n"
        
        prompt += "\nPlease provide:\n"
        prompt += "1. Clean, well-structured code\n"
        prompt += "2. Comments explaining key parts\n"
        prompt += "3. Brief explanation of the implementation\n"
        
        return prompt
    
    def _parse_generation_response(self, response_text: str) -> tuple[str, str]:
        """Parse Gemini response to extract code and explanation"""
        # Try to extract code blocks
        code_pattern = r'```(?:\w+)?\n(.*?)```'
        code_matches = re.findall(code_pattern, response_text, re.DOTALL)
        
        if code_matches:
            generated_code = code_matches[0].strip()
            # Remove code block from explanation
            explanation = re.sub(code_pattern, '', response_text, flags=re.DOTALL).strip()
        else:
            generated_code = response_text
            explanation = "Code generated successfully"
        
        return generated_code, explanation


class CodeReviewService:
    """Service for code review using AI"""
    
    def __init__(self, gemini_repo: Optional[GeminiRepository] = None):
        self.gemini_repo = gemini_repo or GeminiRepository()
    
    def review_code(self, request: CodeReviewRequest) -> CodeReviewResponse:
        try:
            # Call Gemini API for review with specified model
            response_text = self.gemini_repo.review_code(
                code=request.code,
                language=request.language,
                review_type=request.review_type,
                model_name=request.model
            )
            
            # Parse review response
            score, issues, summary, improvements = self._parse_review_response(response_text)
            
            return CodeReviewResponse(
                overall_score=score,
                issues=issues,
                summary=summary,
                improvements=improvements,
                timestamp=datetime.now(),
                success=True
            )
        except Exception as e:
            return CodeReviewResponse(
                overall_score=0.0,
                issues=[],
                summary="",
                improvements=[],
                timestamp=datetime.now(),
                success=False,
                error_message=str(e)
            )
    
    def _parse_review_response(self, response_text: str) -> tuple[float, list, str, list]:
        """Parse review response from Gemini"""
        # Default values
        score = 7.0
        issues = []
        summary = response_text
        improvements = []
        
        # Try to extract score
        score_pattern = r'(?:score|rating)[:\s]+(\d+(?:\.\d+)?)'
        score_match = re.search(score_pattern, response_text, re.IGNORECASE)
        if score_match:
            score = float(score_match.group(1))
        
        # Try to extract issues (simple parsing)
        # You can enhance this with more sophisticated parsing
        issue_keywords = ['bug', 'error', 'issue', 'problem', 'warning']
        lines = response_text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            for keyword in issue_keywords:
                if keyword in line_lower:
                    issues.append(ReviewIssue(
                        severity='medium',
                        line_number=None,
                        issue_type='general',
                        description=line.strip(),
                        suggestion='Review and fix as suggested'
                    ))
                    break
        
        # Extract improvements
        if 'improvement' in response_text.lower() or 'suggest' in response_text.lower():
            improvement_lines = [line.strip() for line in lines if line.strip() and 
                               ('suggest' in line.lower() or 'improve' in line.lower() or 
                                'consider' in line.lower() or 'recommend' in line.lower())]
            improvements = improvement_lines[:5]  # Limit to 5
        
        return score, issues, summary, improvements
