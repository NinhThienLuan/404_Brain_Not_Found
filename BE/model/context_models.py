"""
Context Models
Pydantic models for context parsing
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class FunctionInput(BaseModel):
    """Model for function input parameter"""
    name: str
    type: str
    description: Optional[str] = None


class FunctionOutput(BaseModel):
    """Model for function output"""
    name: Optional[str] = None
    type: str
    description: Optional[str] = None


class ErrorHandling(BaseModel):
    """Model for error handling requirements"""
    expected_errors: List[str] = Field(default_factory=list)
    handling_strategy: Optional[str] = "raise exception"


class ParsedContext(BaseModel):
    """Model for parsed context from user input"""
    user_goal: str = Field(..., description="Main goal of the user")
    purpose: Optional[str] = Field(None, description="Purpose of the function/code")
    function_name: Optional[str] = Field(None, description="Name of the function")
    preferred_language: Optional[str] = Field("python", description="Programming language")
    inputs: List[FunctionInput] = Field(default_factory=list, description="Input parameters")
    outputs: List[FunctionOutput] = Field(default_factory=list, description="Output specifications")
    core_logic: Optional[str] = Field(None, description="Core logic description")
    error_handling: Optional[ErrorHandling] = Field(None, description="Error handling requirements")
    additional_notes: Optional[str] = Field(None, description="Additional notes or constraints")


class ContextParsingRequest(BaseModel):
    """Request model for context parsing"""
    user_context: str = Field(..., description="User's context/requirement in natural language")
    model: str = Field("gemini-1.5-flash", description="Gemini model to use")


class ContextParsingResponse(BaseModel):
    """Response model for context parsing"""
    success: bool
    parsed_context: Optional[ParsedContext] = None
    error: Optional[str] = None
