"""
Context Parsing Service - Trích xuất JSON từ context text
"""
from typing import Dict, Any, Tuple
import json
import re
from datetime import datetime

from BE.repository.gemini_repo import GeminiRepository
from BE.repository.context_repo import ContextRepository
from BE.entities.context_entity import Context
from BE.model.orchestration_models import ContextParseRequest, ContextParseResponse


class ContextParsingService:
    """Service để parse context text thành JSON structure"""
    
    def __init__(self):
        self.gemini_repo = GeminiRepository()
        self.context_repo = ContextRepository()
    
    def parse_context(self, request: ContextParseRequest) -> ContextParseResponse:
        """
        Parse context text thành JSON
        
        Workflow:
        1. Tạo prompt kỹ thuật để LLM trích xuất thông tin
        2. Gọi LLM
        3. Validate và format JSON
        4. Lưu vào database
        5. Return response
        """
        try:
            # 1. Build prompt
            prompt = self._build_parsing_prompt(request.context_text)
            
            # 2. Call LLM
            response_text = self.gemini_repo.generate_code(prompt, model_name=request.model)
            
            # 3. Extract and validate JSON
            parsed_json, confidence = self._extract_and_validate_json(response_text)
            
            # 4. Save to database
            context = Context(
                session_id=request.session_id,
                raw_text=request.context_text,
                parsed_json=parsed_json,
                parsing_model=request.model,
                confidence_score=confidence
            )
            saved_context = self.context_repo.create(context)
            
            # 5. Return response
            return ContextParseResponse(
                session_id=request.session_id,
                parsed_json=parsed_json,
                confidence_score=confidence,
                success=True,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return ContextParseResponse(
                session_id=request.session_id,
                parsed_json={},
                confidence_score=0.0,
                success=False,
                error_message=str(e),
                timestamp=datetime.now()
            )
    
    def _build_parsing_prompt(self, context_text: str) -> str:
        """Tạo prompt kỹ thuật để trích xuất JSON"""
        prompt = f"""
Bạn là một AI chuyên trích xuất thông tin từ mô tả yêu cầu và chuyển thành JSON structure.

Từ mô tả sau, hãy trích xuất thông tin thành JSON với các key sau:
- "topic": Chủ đề chính của yêu cầu
- "main_function": Chức năng chính cần xây dựng
- "sub_functions": Danh sách các chức năng phụ (array)
- "input_data": Mô tả dữ liệu đầu vào
- "output_data": Mô tả dữ liệu đầu ra
- "technology": Công nghệ/framework được đề cập (nếu có)
- "additional_requirements": Các yêu cầu bổ sung (array)

MÔ TẢ TỪ USER:
{context_text}

Hãy trả về CHÍNH XÁC format JSON như sau (không thêm text gì khác):
```json
{{
    "topic": "...",
    "main_function": "...",
    "sub_functions": ["...", "..."],
    "input_data": "...",
    "output_data": "...",
    "technology": "...",
    "additional_requirements": ["...", "..."]
}}
```
"""
        return prompt
    
    def _extract_and_validate_json(self, response_text: str) -> Tuple[Dict[str, Any], float]:
        """
        Trích xuất và validate JSON từ response
        
        Returns:
            Tuple[Dict, float]: (parsed_json, confidence_score)
        """
        # Extract JSON from markdown code block
        json_pattern = r'```json\s*\n(.*?)\n```'
        match = re.search(json_pattern, response_text, re.DOTALL)
        
        if match:
            json_str = match.group(1)
        else:
            # Try to find JSON object directly
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, response_text, re.DOTALL)
            if match:
                json_str = match.group(0)
            else:
                raise ValueError("Could not extract JSON from response")
        
        # Parse JSON
        try:
            parsed_json = json.loads(json_str)
            
            # Validate required keys
            required_keys = ["topic", "main_function", "input_data", "output_data"]
            confidence = 1.0
            
            for key in required_keys:
                if key not in parsed_json or not parsed_json[key]:
                    confidence -= 0.2
            
            # Ensure arrays are arrays
            if "sub_functions" in parsed_json and not isinstance(parsed_json["sub_functions"], list):
                parsed_json["sub_functions"] = [parsed_json["sub_functions"]]
            
            if "additional_requirements" in parsed_json and not isinstance(parsed_json["additional_requirements"], list):
                parsed_json["additional_requirements"] = [parsed_json["additional_requirements"]]
            
            confidence = max(0.0, min(1.0, confidence))
            
            return parsed_json, confidence
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

