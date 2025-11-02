"""
Context Parsing Service (Service 1)
"""

import json
import logging
from typing import Optional, Dict, Any

from model.intent_models import ParsedContextV2, GoalType
from repository.gemini_repo import GeminiRepository


class ContextParsingService:
    """Service trích xuất context một lần từ user message"""

    def __init__(self, gemini_repo: Optional[GeminiRepository] = None):
        self.gemini_repo = gemini_repo or GeminiRepository()
        self.logger = logging.getLogger(__name__)

    def extract_one_shot(self, user_context: str, model_name: Optional[str] = None):
        """Trích xuất context một lần từ user message"""
        try:
            prompt = self._build_extraction_prompt(user_context)
            response_text = self.gemini_repo.generate_code(prompt, model_name=model_name)
            extracted_data = self._parse_json_response(response_text)

            if not extracted_data:
                return False, None, "Failed to parse JSON response from Gemini"

            return True, self._convert_to_parsed_context(extracted_data), None

        except Exception as e:
            self.logger.error(f"Error in extract_one_shot: {str(e)}")
            return False, None, str(e)

    def _build_extraction_prompt(self, user_context: str) -> str:
        """Build prompt theo template"""
        template = """Ban la mot Ky su Cau noi AI chuyen nghiep.

CONTEXT DAU VAO
{user_context}

CAU TRUC JSON MUC TIEU
{{
  "function_name": "Ten ham goi y",
  "purpose": "Mo ta muc dich chinh",
  "inputs": [{{"name": "ten", "type": "kieu", "description": "mo ta"}}],
  "core_logic": ["Buoc 1", "Buoc 2"],
  "outputs": {{"type": "kieu", "description": "mo ta"}}
}}

QUY TAC:
- CHI TRA VE JSON, khong giai thich
- Neu thieu thong tin: null hoac []
- Dam bao JSON hop le"""
        
        return template.format(user_context=user_context)

    def _parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON from response"""
        try:
            if not response_text:
                self.logger.error("Response text is None or empty")
                return None
            
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                self.logger.warning(f"No JSON found in response: {response_text[:200] if response_text else 'None'}")
                return None

            json_str = response_text[json_start:json_end]
            data = json.loads(json_str)

            required_keys = ['function_name', 'purpose', 'inputs', 'core_logic', 'outputs']
            if not all(key in data for key in required_keys):
                return None

            return data

        except Exception as e:
            self.logger.error(f"Parse error: {e}")
            return None

    def _convert_to_parsed_context(self, extracted_data: Dict[str, Any]) -> ParsedContextV2:
        """Convert to ParsedContextV2"""
        try:
            inputs = []
            if extracted_data.get('inputs'):
                for item in extracted_data['inputs']:
                    if isinstance(item, dict):
                        inputs.append({
                            "name": item.get("name", ""),
                            "type": item.get("type", "str"),
                            "description": item.get("description", "")
                        })

            core_logic = extracted_data.get('core_logic', [])
            if not isinstance(core_logic, list):
                core_logic = [str(core_logic)] if core_logic else []

            outputs = None
            if extracted_data.get('outputs') and isinstance(extracted_data['outputs'], dict):
                outputs = {
                    "type": extracted_data['outputs'].get("type", "void"),
                    "description": extracted_data['outputs'].get("description", "")
                }

            function_details = {
                "function_name": extracted_data.get("function_name"),
                "purpose": extracted_data.get("purpose"),
                "inputs": inputs,
                "core_logic": core_logic,
                "outputs": outputs,
                "error_handling": []
            }

            return ParsedContextV2(
                goal_type=GoalType.GENERATE_FUNCTION,
                details=function_details
            )

        except Exception as e:
            self.logger.error(f"Convert error: {e}")
            return None
