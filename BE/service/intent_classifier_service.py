"""
Intent Classifier Service - Bộ Điều phối Chính
Service "não bộ" điều phối luồng nghiệp vụ
"""
from typing import Dict, Any, Optional, Tuple
import json
import re

from model.intent_models import (
    IntentType,
    IntentClassifierRequest,
    IntentClassifierResponse,
    ParsedContextV2
)


class IntentClassifierService:
    """
    Bộ điều phối chính - Intent Classifier Service
    Nhận user_message và session_id, quyết định intent và data
    """

    def __init__(self):
        """Khởi tạo service với các dependencies"""
        # TODO: Inject these services when they exist
        self.context_parsing_service = None  # ContextParsingService()
        self.context_refinement_service = None  # ContextRefinementService()
        self.state_management_service = None  # StateManagementService()

    def classify_intent(self, request: IntentClassifierRequest) -> IntentClassifierResponse:
        """
        Phân loại intent chính - Logic điều phối

        Args:
            request: IntentClassifierRequest chứa user_message và session_id

        Returns:
            IntentClassifierResponse với intent và data
        """
        user_message = request.user_message.strip()
        session_id = request.session_id

        # Tải facts từ StateManagementService
        facts = self._load_facts(session_id)

        # Luồng A: Đang hỏi dở dang (state tồn tại)
        if facts:
            return self._handle_ongoing_refinement(user_message, facts, session_id)

        # Luồng B: Yêu cầu mới (state không tồn tại)
        else:
            return self._handle_new_request(user_message, session_id)

    def _load_facts(self, session_id: str) -> Optional[ParsedContextV2]:
        """
        Tải facts từ StateManagementService
        TODO: Implement khi StateManagementService có sẵn
        """
        # Placeholder - tạm thời return None
        return None

    def _handle_ongoing_refinement(
        self,
        user_message: str,
        facts: ParsedContextV2,
        session_id: str
    ) -> IntentClassifierResponse:
        """
        Xử lý luồng A: Đang hỏi dở dang
        """
        # Gọi ContextRefinementService.handle_reply()
        # TODO: Implement khi ContextRefinementService có sẵn

        # Placeholder logic
        # Giả sử facts đã đủ
        if self._is_facts_complete(facts):
            # Trả về (INTENT_GENERATE_CODE, completed_json)
            self._delete_state(session_id)  # Xóa state
            return IntentClassifierResponse(
                intent=IntentType.GENERATE_CODE,
                data={"completed_json": facts.dict()},
                session_id=session_id,
                completed_json=facts
            )
        else:
            # Trả về (INTENT_REFINE_CONTEXT, next_question)
            next_question = self._get_next_question(facts)
            self._update_state(session_id, facts)  # Cập nhật state
            return IntentClassifierResponse(
                intent=IntentType.REFINE_CONTEXT,
                data={"next_question": next_question},
                session_id=session_id,
                next_question=next_question
            )

    def _handle_new_request(self, user_message: str, session_id: str) -> IntentClassifierResponse:
        """
        Xử lý luồng B: Yêu cầu mới
        """
        # Kiểm tra nhanh xem có phải yêu cầu sửa code không
        if self._is_modify_code_request(user_message):
            return IntentClassifierResponse(
                intent=IntentType.MODIFY_CODE,
                data={"user_message": user_message},
                session_id=session_id
            )

        # Gọi ContextParsingService.extract_one_shot()
        # TODO: Implement khi ContextParsingService có sẵn

        # Placeholder: Giả sử trích xuất thành công
        parsed_json = self._mock_extract_context(user_message)

        if not parsed_json:
            # Trích xuất lỗi - CHITCHAT
            return IntentClassifierResponse(
                intent=IntentType.CHITCHAT,
                data={"response_message": "Chào bạn, bạn cần tôi tạo code gì?"},
                session_id=session_id,
                response_message="Chào bạn, bạn cần tôi tạo code gì?"
            )

        # Kiểm tra parsed_json có đủ thông tin không
        if self._is_context_complete(parsed_json):
            # Đủ thông tin
            return IntentClassifierResponse(
                intent=IntentType.GENERATE_CODE,
                data={"completed_json": parsed_json.dict()},
                session_id=session_id,
                completed_json=parsed_json
            )
        else:
            # Thiếu thông tin
            # Lưu parsed_json vào StateManagementService
            self._save_facts(session_id, parsed_json)

            # Gọi ContextRefinementService.start_refinement()
            first_question = self._get_first_question(parsed_json)

            return IntentClassifierResponse(
                intent=IntentType.REFINE_CONTEXT,
                data={"first_question": first_question},
                session_id=session_id,
                next_question=first_question
            )

    # ============ Helper Methods ============

    def _is_modify_code_request(self, user_message: str) -> bool:
        """Kiểm tra nhanh xem có phải yêu cầu sửa code không"""
        modify_keywords = [
            "sửa", "fix", "chỉnh sửa", "thay đổi", "cập nhật",
            "modify", "update", "change", "correct", "improve"
        ]

        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in modify_keywords)

    def _mock_extract_context(self, user_message: str) -> Optional[ParsedContextV2]:
        """Mock extraction - TODO: Replace with real ContextParsingService"""
        # Simple mock logic
        if "tạo" in user_message.lower() or "create" in user_message.lower():
            # Mock a simple function context
            from model.intent_models import GoalType, FunctionDetails
            return ParsedContextV2(
                goal_type=GoalType.GENERATE_FUNCTION,
                details={
                    "function_name": "example_function",
                    "purpose": "Example function",
                    "inputs": [],
                    "core_logic": ["Basic logic"],
                    "outputs": {"type": "str", "description": "Result"},
                    "error_handling": []
                }
            )
        return None

    def _is_facts_complete(self, facts: ParsedContextV2) -> bool:
        """Kiểm tra facts đã đủ chưa"""
        return facts.is_complete()

    def _is_context_complete(self, context: ParsedContextV2) -> bool:
        """Kiểm tra context đã đủ chưa"""
        return context.is_complete()

    def _get_next_question(self, facts: ParsedContextV2) -> str:
        """Lấy câu hỏi tiếp theo"""
        missing = facts.get_missing_fields()
        if "function_name" in missing:
            return "Bạn muốn đặt tên hàm là gì?"
        elif "purpose" in missing:
            return "Hàm này dùng để làm gì?"
        elif "inputs" in missing:
            return "Hàm cần những tham số đầu vào nào?"
        elif "core_logic" in missing:
            return "Logic chính của hàm như thế nào?"
        else:
            return "Bạn có thể cho thêm chi tiết không?"

    def _get_first_question(self, context: ParsedContextV2) -> str:
        """Lấy câu hỏi đầu tiên cho refinement"""
        missing = context.get_missing_fields()
        if missing:
            return self._get_next_question(context)
        return "Bạn có thể cho thêm chi tiết không?"

    def _save_facts(self, session_id: str, facts: ParsedContextV2):
        """Lưu facts vào StateManagementService"""
        # TODO: Implement khi StateManagementService có sẵn
        pass

    def _update_state(self, session_id: str, facts: ParsedContextV2):
        """Cập nhật state"""
        # TODO: Implement khi StateManagementService có sẵn
        self._save_facts(session_id, facts)

    def _delete_state(self, session_id: str):
        """Xóa state"""
        # TODO: Implement khi StateManagementService có sẵn
        pass