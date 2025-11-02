"""
CodeGeneration Service
"""
from typing import Dict, Optional
from BE.service.base_service import BaseService
from BE.repository.code_generation_repo import CodeGenerationRepository
from BE.entities.code_generation_entity import CodeGeneration
import json
from typing import Any


class CodeGenerationService(BaseService[CodeGeneration]):
    """Service cho CodeGeneration"""
    
    def __init__(self):
        super().__init__(CodeGenerationRepository())
    
    def get_by_request(self, request_id: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code generations theo request_id"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_request(request_id, skip=skip, limit=page_size)
        total = self.repo.count({"request_id": request_id})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    
    def get_by_status(self, status: str, page: int = 1, page_size: int = 10) -> Dict:
        """Lấy code generations theo status"""
        page = max(1, page)
        page_size = max(1, min(100, page_size))
        skip = (page - 1) * page_size
        
        items = self.repo.find_by_status(status, skip=skip, limit=page_size)
        total = self.repo.count({"status": status})
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

    # ------------------------------
    # Mock / placeholder for requirement-based generation
    # ------------------------------
    # Tạm thời chèn một ví dụ JSON requirement (commented) để dễ dàng test tính năng
    # Cập nhật sau: nhận requirement thực tế từ IntentClassifierService
    # Example requirement JSON (commented out):
    # {
    #   "request_id": "req_12345",
    #   "language": "python",
    #   "task": "Tạo hàm tính giai thừa",
    #   "constraints": {
    #       "max_lines": 50,
    #       "style": "clear and documented"
    #   },
    #   "examples": [
    #       {"input": 5, "output": 120}
    #   ]
    # }

    def _build_prompt_from_requirement(self, requirement: Dict) -> str:
        """Create a human-readable prompt for Gemini from the requirement JSON."""
        try:
            lang = requirement.get("language", "python")
            task = requirement.get("task", "Viết mã theo yêu cầu sau")
            constraints = requirement.get("constraints", {})
            examples = requirement.get("examples", [])

            prompt_parts = [
                f"You are a helpful code generator. Produce {lang} code.",
                f"Requirement: {task}",
            ]

            if constraints:
                prompt_parts.append("Constraints:")
                for k, v in constraints.items():
                    prompt_parts.append(f"- {k}: {v}")

            if examples:
                prompt_parts.append("Examples:")
                for ex in examples:
                    prompt_parts.append(f"- input: {ex.get('input')}, expected output: {ex.get('output')}")

            # Encourage compact, documented code
            prompt_parts.append("Please provide only the code block and brief comments describing the approach.")

            return "\n".join(prompt_parts)
        except Exception:
            # Fallback simple prompt
            return json.dumps(requirement, ensure_ascii=False)

    def generate_from_requirement(self, requirement: Dict) -> Dict:
        """Generate code from a requirement JSON using Gemini.

        This method is safe to call even when Gemini API key is not configured:
        - If Gemini is available, it will call the client and return the model output.
        - Otherwise it returns a mock response (commented placeholder) so callers/tests can proceed.

        Returns: {"prompt": str, "response": str}
        """
        prompt = self._build_prompt_from_requirement(requirement)

        # Try to use Gemini client; if not available (no API key / errors) return mock text
        try:
            # Import here to avoid raising at module import time if GEMINI_API_KEY missing
            from BE.utils.gemini_client import gemini_ai

            # Call Gemini to generate content. Parameters can be adjusted later.
            gen_result = gemini_ai.generate_content(prompt, temperature=0.2, max_output_tokens=800)

            # The `gen_result` type depends on the Gemini client; attempt to extract text content
            # If the object has a `text` attribute (or similar), use it; otherwise stringify.
            response_text = None
            if hasattr(gen_result, "text"):
                response_text = getattr(gen_result, "text")
            elif isinstance(gen_result, dict) and "candidates" in gen_result:
                # Some SDKs return dicts with candidates
                try:
                    response_text = gen_result.get("candidates")[0].get("content")
                except Exception:
                    response_text = str(gen_result)
            else:
                response_text = str(gen_result)

        except Exception as e:
            # Return a mock response (clearly marked) so that tests and early integrations can run
            response_text = (
                f"[MOCK_RESPONSE] Gemini unavailable or error: {e}\n"
                "# MOCK GENERATED CODE START\n"
                "def placeholder():\n"
                "    \"\"\"This is a mock implementation. Replace with real Gemini output.\"\"\"\n"
                "    return None\n"
                "# MOCK GENERATED CODE END"
            )

        return {"prompt": prompt, "response": response_text}

    def generate_from_user_context(self, user_context: str, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Extract requirement from user context via ContextParsingService and generate code.

        Returns a dict with keys:
          - ok: bool
          - error: optional error message
          - requirement: parsed requirement (if ok)
          - generation: output from generate_from_requirement (if ok)
        """
        try:
            # Local import to avoid circular imports at module load time
            from BE.service.context_parsing_service import ContextParsingService

            cps = ContextParsingService()
            ok, parsed_ctx, err = cps.extract_one_shot(user_context, model_name=model_name)

            if not ok:
                return {"ok": False, "error": err}

            # parsed_ctx is a ParsedContextV2-like object with `details`
            details = getattr(parsed_ctx, "details", parsed_ctx)

            # Build a generic requirement dict from parsed details
            requirement = {
                "request_id": details.get("request_id") if isinstance(details, dict) else None,
                "language": "python",
                "task": details.get("purpose") if isinstance(details, dict) else None,
                "constraints": {},
                "examples": [],
                "function_name": details.get("function_name") if isinstance(details, dict) else None,
                "inputs": details.get("inputs") if isinstance(details, dict) else [],
                "core_logic": details.get("core_logic") if isinstance(details, dict) else [],
                "outputs": details.get("outputs") if isinstance(details, dict) else None,
            }

            generation = self.generate_from_requirement(requirement)

            return {"ok": True, "requirement": requirement, "generation": generation}

        except Exception as e:
            return {"ok": False, "error": str(e)}
