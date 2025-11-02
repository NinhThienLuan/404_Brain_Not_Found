from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum


class IntentType(str, Enum):
    """Types of user intents"""
    REFINE_CONTEXT = "INTENT_REFINE_CONTEXT"
    GENERATE_CODE = "INTENT_GENERATE_CODE"
    MODIFY_CODE = "INTENT_MODIFY_CODE"
    CHITCHAT = "INTENT_CHITCHAT"
    GENERATE_LAYOUT = "INTENT_GENERATE_LAYOUT"


class GoalType(str, Enum):
    """Goal types for context parsing"""
    GENERATE_FUNCTION = "GENERATE_FUNCTION"
    GENERATE_MULTIPLE_FUNCTIONS = "GENERATE_MULTIPLE_FUNCTIONS"  # New: Multiple functions at once
    GENERATE_LAYOUT = "GENERATE_LAYOUT"


# ============ FUNCTION MODELS ============

class FunctionInputDetail(BaseModel):
    """Detailed function input parameter"""
    name: str = Field(..., description="Tên tham số")
    type: str = Field(..., description="Kiểu dữ liệu")
    description: str = Field(..., description="Mô tả tham số")


class FunctionOutputDetail(BaseModel):
    """Function output specification"""
    type: str = Field(..., description="Kiểu dữ liệu trả về")
    description: str = Field(..., description="Mô tả giá trị trả về")


class ErrorHandlingDetail(BaseModel):
    """Error handling specification"""
    condition: str = Field(..., description="Điều kiện lỗi")
    action: str = Field(..., description="Hành động xử lý")


class FunctionDetails(BaseModel):
    """Details for GENERATE_FUNCTION goal (single function)"""
    function_name: Optional[str] = Field(None, description="Tên hàm gợi ý")
    purpose: Optional[str] = Field(None, description="Mô tả mục đích chính của hàm")
    inputs: List[FunctionInputDetail] = Field(default_factory=list, description="Danh sách tham số đầu vào")
    core_logic: List[str] = Field(default_factory=list, description="Các bước xử lý logic chính")
    outputs: Optional[FunctionOutputDetail] = Field(None, description="Thông tin đầu ra")
    error_handling: List[ErrorHandlingDetail] = Field(default_factory=list, description="Xử lý lỗi")


class MultipleFunctionsDetails(BaseModel):
    """Details for GENERATE_MULTIPLE_FUNCTIONS goal (e.g., CRUD, API set)"""
    group_name: Optional[str] = Field(None, description="Tên nhóm function (ví dụ: 'User CRUD', 'Payment API')")
    description: Optional[str] = Field(None, description="Mô tả tổng quan về nhóm function")
    shared_context: Optional[str] = Field(None, description="Context chung (ví dụ: 'User model có: id, name, email')")
    functions: List[FunctionDetails] = Field(default_factory=list, description="Danh sách các function cần tạo")


# ============ LAYOUT MODELS ============

class ComponentDetail(BaseModel):
    """UI Component specification"""
    type: str = Field(..., description="Loại component: title, input, button, text")
    text: Optional[str] = Field(None, description="Nội dung text")
    placeholder: Optional[str] = Field(None, description="Text giữ chỗ (cho input)")
    identifier: Optional[str] = Field(None, description="Tên/ID gợi ý")


class LayoutStructure(BaseModel):
    """Layout structure specification"""
    alignment: Optional[str] = Field(None, description="Căn chỉnh (ví dụ: căn giữa)")
    structure: Optional[str] = Field(None, description="Mô tả cấu trúc/thứ tự các thành phần")


class StyleDetail(BaseModel):
    """Style specification"""
    colors: Optional[str] = Field(None, description="Mô tả màu sắc")
    font: Optional[str] = Field(None, description="Mô tả font")
    other: List[str] = Field(default_factory=list, description="Mô tả style khác")


class LayoutDetails(BaseModel):
    """Details for GENERATE_LAYOUT goal"""
    page_name: Optional[str] = Field(None, description="Tên trang hoặc thành phần")
    components: List[ComponentDetail] = Field(default_factory=list, description="Danh sách components")
    layout: Optional[LayoutStructure] = Field(None, description="Cấu trúc layout")
    style: Optional[StyleDetail] = Field(None, description="Thông tin style")


# ============ UNIFIED PARSED CONTEXT ============

class ParsedContextV2(BaseModel):
    """
    Unified context structure supporting both FUNCTION and LAYOUT
    Cấu trúc JSON Mục tiêu thống nhất
    """
    goal_type: GoalType = Field(..., description="Loại mục tiêu: GENERATE_FUNCTION hoặc GENERATE_LAYOUT")
    details: Dict[str, Any] = Field(..., description="Chi tiết theo goal_type")
    
    def get_function_details(self) -> Optional[FunctionDetails]:
        """Get details as FunctionDetails if goal_type is GENERATE_FUNCTION"""
        if self.goal_type == GoalType.GENERATE_FUNCTION:
            return FunctionDetails(**self.details)
        return None
    
    def get_multiple_functions_details(self) -> Optional[MultipleFunctionsDetails]:
        """Get details as MultipleFunctionsDetails if goal_type is GENERATE_MULTIPLE_FUNCTIONS"""
        if self.goal_type == GoalType.GENERATE_MULTIPLE_FUNCTIONS:
            return MultipleFunctionsDetails(**self.details)
        return None
    
    def get_layout_details(self) -> Optional[LayoutDetails]:
        """Get details as LayoutDetails if goal_type is GENERATE_LAYOUT"""
        if self.goal_type == GoalType.GENERATE_LAYOUT:
            return LayoutDetails(**self.details)
        return None
    
    def is_complete(self) -> bool:
        """Check if context has sufficient information"""
        if self.goal_type == GoalType.GENERATE_FUNCTION:
            func_details = self.get_function_details()
            if not func_details:
                return False
            # Consider complete if has at least: purpose and some inputs or core_logic
            return bool(func_details.purpose and (func_details.inputs or func_details.core_logic))
        
        elif self.goal_type == GoalType.GENERATE_MULTIPLE_FUNCTIONS:
            multi_details = self.get_multiple_functions_details()
            if not multi_details:
                return False
            # Consider complete if has: group_name and at least 1 function with purpose
            if not multi_details.group_name or not multi_details.functions:
                return False
            # Check if at least some functions have basic info
            return any(f.purpose for f in multi_details.functions)
        
        elif self.goal_type == GoalType.GENERATE_LAYOUT:
            layout_details = self.get_layout_details()
            if not layout_details:
                return False
            # Consider complete if has at least: page_name and some components
            return bool(layout_details.page_name and layout_details.components)
        
        return False
    
    def get_missing_fields(self) -> List[str]:
        """Get list of missing critical fields"""
        missing = []
        
        if self.goal_type == GoalType.GENERATE_FUNCTION:
            func_details = self.get_function_details()
            if not func_details:
                return ["all_fields"]
            
            if not func_details.function_name:
                missing.append("function_name")
            if not func_details.purpose:
                missing.append("purpose")
            if not func_details.inputs:
                missing.append("inputs")
            if not func_details.core_logic:
                missing.append("core_logic")
            if not func_details.outputs:
                missing.append("outputs")
        
        elif self.goal_type == GoalType.GENERATE_MULTIPLE_FUNCTIONS:
            multi_details = self.get_multiple_functions_details()
            if not multi_details:
                return ["all_fields"]
            
            if not multi_details.group_name:
                missing.append("group_name")
            if not multi_details.shared_context:
                missing.append("shared_context")
            if not multi_details.functions:
                missing.append("functions")
            else:
                # Check if functions have enough detail
                incomplete_funcs = [f for f in multi_details.functions if not f.purpose]
                if incomplete_funcs:
                    missing.append("function_details")
        
        elif self.goal_type == GoalType.GENERATE_LAYOUT:
            layout_details = self.get_layout_details()
            if not layout_details:
                return ["all_fields"]
            
            if not layout_details.page_name:
                missing.append("page_name")
            if not layout_details.components:
                missing.append("components")
            if not layout_details.layout:
                missing.append("layout")
            if not layout_details.style:
                missing.append("style")
        
        return missing


# ============ INTENT CLASSIFIER MODELS ============

class IntentClassifierRequest(BaseModel):
    """Request for intent classification"""
    user_message: str = Field(..., description="Tin nhắn mới từ người dùng")
    session_id: str = Field(..., description="ID phiên để lưu trữ state")


class IntentClassifierResponse(BaseModel):
    """Response from intent classifier"""
    intent: IntentType = Field(..., description="Ý định được phân loại")
    data: Dict[str, Any] = Field(..., description="Dữ liệu đi kèm")
    session_id: str = Field(..., description="ID phiên")
    
    # Helper fields for specific intents
    next_question: Optional[str] = Field(None, description="Câu hỏi tiếp theo (nếu intent là REFINE_CONTEXT)")
    completed_json: Optional[ParsedContextV2] = Field(None, description="JSON hoàn chỉnh (nếu intent là GENERATE_CODE)")
    response_message: Optional[str] = Field(None, description="Tin nhắn phản hồi (nếu intent là CHITCHAT)")


# ============ CONTEXT REFINEMENT MODELS ============

class RefinementRequest(BaseModel):
    """Request for context refinement"""
    user_reply: Optional[str] = Field(None, description="Câu trả lời mới của user")
    current_facts: ParsedContextV2 = Field(..., description="Facts hiện tại đang thiếu")


class RefinementResponse(BaseModel):
    """Response from context refinement"""
    is_complete: bool = Field(..., description="Có đủ thông tin chưa")
    next_question: Optional[str] = Field(None, description="Câu hỏi tiếp theo nếu chưa đủ")
    updated_facts: ParsedContextV2 = Field(..., description="Facts đã được cập nhật")
    completed: bool = Field(default=False, description="Đã hoàn thành refinement")
