"""
Agent Orchestration Service - Điều phối các luồng công việc
"""
from typing import Optional
from datetime import datetime

from BE.repository.session_repo import SessionRepository
from BE.repository.context_repo import ContextRepository
from BE.repository.gemini_repo import GeminiRepository
from BE.entities.session_entity import Session, WorkflowStep
from BE.service.context_parsing_service import ContextParsingService
from BE.service.ai_service import CodeGenerationService
from BE.model.orchestration_models import (
    AgentRequest,
    AgentResponse,
    SessionCreateRequest,
    SessionResponse,
    IntentClassifyRequest,
    IntentClassifyResponse,
    IntentType,
    ContextParseRequest
)
from BE.model.ai_models import CodeGenerationRequest


class AgentOrchestrationService:
    """
    Service điều phối chính
    
    Quản lý:
    - State của session
    - Luồng F1: Parse context
    - Luồng F2: Classify intent + Generate code
    - Luồng F3: Analyze code
    """
    
    def __init__(self):
        self.session_repo = SessionRepository()
        self.context_repo = ContextRepository()
        self.gemini_repo = GeminiRepository()
        self.context_parsing_service = ContextParsingService()
        self.code_gen_service = CodeGenerationService()
    
    # ==================== SESSION MANAGEMENT ====================
    
    def create_session(self, request: SessionCreateRequest) -> SessionResponse:
        """Tạo session mới cho user"""
        try:
            now = datetime.now()
            session = Session(
                user_id=request.user_id,
                current_step=WorkflowStep.IDLE,
                metadata=request.metadata or {},
                created_at=now,
                updated_at=now
            )
            
            saved_session = self.session_repo.create(session)
            
            return SessionResponse(
                session_id=saved_session.id,
                user_id=saved_session.user_id,
                current_step=saved_session.current_step.value,
                context_json=saved_session.context_json,
                code_history=saved_session.code_history,
                created_at=saved_session.created_at or now,
                updated_at=saved_session.updated_at or now
            )
        except Exception as e:
            raise Exception(f"Failed to create session: {str(e)}")
    
    def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Lấy thông tin session"""
        session = self.session_repo.find_by_id(session_id)
        if not session:
            return None
        
        return SessionResponse(
            session_id=session.id,
            user_id=session.user_id,
            current_step=session.current_step.value,
            context_json=session.context_json,
            code_history=session.code_history,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    
    # ==================== FLOW 1: PARSE CONTEXT ====================
    
    def process_context(self, session_id: str, context_text: str, model: str = "gemini-2.5-flash") -> AgentResponse:
        """
        Luồng F1: Nhận context và parse thành JSON
        """
        try:
            # Update session step
            self.session_repo.update_step(session_id, WorkflowStep.PARSING_CONTEXT)
            
            # Parse context using ContextParsingService.extract_one_shot
            # NOTE: ContextParsingService provides `extract_one_shot(user_context, model_name)` which
            # returns (ok: bool, parsed_ctx: ParsedContextV2, err: Optional[str])
            ok, parsed_ctx, err = self.context_parsing_service.extract_one_shot(context_text, model_name=model)

            if not ok:
                self.session_repo.update_step(session_id, WorkflowStep.ERROR)
                return AgentResponse(
                    session_id=session_id,
                    current_step=WorkflowStep.ERROR.value,
                    success=False,
                    message="Failed to parse context",
                    error_message=err,
                    timestamp=datetime.now()
                )

            # Convert parsed_ctx (ParsedContextV2) to plain JSON/dict for storage
            parsed_json = parsed_ctx.dict() if hasattr(parsed_ctx, "dict") else parsed_ctx

            # Update session with parsed context
            session = self.session_repo.find_by_id(session_id)
            if session:
                session.context_json = parsed_json
                self.session_repo.update(session)

            # Immediately orchestrate to code generation if the parsed goal is to generate code
            try:
                # Update step
                self.session_repo.update_step(session_id, WorkflowStep.GENERATING_CODE)

                # Build a CodeGenerationRequest from parsed context
                # For function generation, include purpose, inputs, core_logic, outputs
                details = parsed_json.get("details", {}) if isinstance(parsed_json, dict) else {}
                goal_type = parsed_json.get("goal_type") if isinstance(parsed_json, dict) else None

                prompt_parts = []
                if goal_type:
                    prompt_parts.append(f"Goal: {goal_type}")

                # Prefer human-readable purpose
                purpose = details.get("purpose") or details.get("description") or "Please implement the requested functionality."
                prompt_parts.append(f"Purpose: {purpose}")

                if details.get("function_name"):
                    prompt_parts.append(f"Function name: {details.get('function_name')}")

                if details.get("inputs"):
                    prompt_parts.append("Inputs:")
                    for inp in details.get("inputs"):
                        prompt_parts.append(f"- {inp}")

                if details.get("core_logic"):
                    prompt_parts.append("Core logic steps:")
                    for step in details.get("core_logic"):
                        prompt_parts.append(f"- {step}")

                if details.get("outputs"):
                    prompt_parts.append(f"Outputs: {details.get('outputs')}")

                prompt = "\n".join(prompt_parts)

                code_request = CodeGenerationRequest(
                    prompt=prompt,
                    language="python",
                    additional_context=str(session.context_json) if session and session.context_json else None,
                    model=model
                )

                code_response = self.code_gen_service.generate_code(code_request)

                if not code_response.success:
                    self.session_repo.update_step(session_id, WorkflowStep.ERROR)
                    return AgentResponse(
                        session_id=session_id,
                        current_step=WorkflowStep.ERROR.value,
                        success=False,
                        message="Code generation failed",
                        error_message=code_response.error_message,
                        timestamp=datetime.now()
                    )

                # Save generated code to session history
                if session:
                    session.add_code_to_history(
                        code=code_response.generated_code,
                        language=code_response.language,
                        description=purpose
                    )
                    session.current_step = WorkflowStep.COMPLETED
                    self.session_repo.update(session)

                return AgentResponse(
                    session_id=session_id,
                    current_step=WorkflowStep.COMPLETED.value,
                    generated_code=code_response.generated_code,
                    context_json=session.context_json if session else parsed_json,
                    success=True,
                    message="Context parsed and code generated successfully",
                    timestamp=datetime.now()
                )
            except Exception as e:
                self.session_repo.update_step(session_id, WorkflowStep.ERROR)
                return AgentResponse(
                    session_id=session_id,
                    current_step=WorkflowStep.ERROR.value,
                    success=False,
                    message="Error during code generation orchestration",
                    error_message=str(e),
                    timestamp=datetime.now()
                )
            
        except Exception as e:
            self.session_repo.update_step(session_id, WorkflowStep.ERROR)
            return AgentResponse(
                session_id=session_id,
                current_step=WorkflowStep.ERROR.value,
                success=False,
                message="Error processing context",
                error_message=str(e),
                timestamp=datetime.now()
            )
    
    # ==================== FLOW 2: CLASSIFY INTENT + GENERATE CODE ====================
    
    def process_prompt(self, request: AgentRequest) -> AgentResponse:
        """
        Luồng F2: Nhận prompt, classify intent, generate code
        """
        try:
            session = self.session_repo.find_by_id(request.session_id)
            if not session:
                return AgentResponse(
                    session_id=request.session_id,
                    current_step=WorkflowStep.ERROR.value,
                    success=False,
                    message="Session not found",
                    timestamp=datetime.now()
                )
            
            # Step 1: Classify intent
            self.session_repo.update_step(request.session_id, WorkflowStep.CLASSIFYING_INTENT)
            
            intent_request = IntentClassifyRequest(
                prompt=request.prompt,
                context_json=session.context_json
            )
            intent_response = self.classify_intent(intent_request)
            
            # Step 2: Generate code based on intent
            self.session_repo.update_step(request.session_id, WorkflowStep.GENERATING_CODE)
            
            code_request = CodeGenerationRequest(
                prompt=request.prompt,
                language="python",
                additional_context=str(session.context_json) if session.context_json else None,
                model=request.model
            )
            code_response = self.code_gen_service.generate_code(code_request)
            
            if not code_response.success:
                self.session_repo.update_step(request.session_id, WorkflowStep.ERROR)
                return AgentResponse(
                    session_id=request.session_id,
                    current_step=WorkflowStep.ERROR.value,
                    success=False,
                    message="Code generation failed",
                    error_message=code_response.error_message,
                    timestamp=datetime.now()
                )
            
            # Save to history
            session.add_code_to_history(
                code=code_response.generated_code,
                language=code_response.language,
                description=request.prompt
            )
            session.last_intent = intent_response.intent.value
            session.last_prompt = request.prompt
            session.current_step = WorkflowStep.COMPLETED
            self.session_repo.update(session)
            
            return AgentResponse(
                session_id=request.session_id,
                current_step=WorkflowStep.COMPLETED.value,
                intent=intent_response.intent.value,
                generated_code=code_response.generated_code,
                context_json=session.context_json,
                success=True,
                message="Code generated successfully",
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.session_repo.update_step(request.session_id, WorkflowStep.ERROR)
            return AgentResponse(
                session_id=request.session_id,
                current_step=WorkflowStep.ERROR.value,
                success=False,
                message="Error processing prompt",
                error_message=str(e),
                timestamp=datetime.now()
            )
    
    def classify_intent(self, request: IntentClassifyRequest) -> IntentClassifyResponse:
        """Classify user intent: create_new, modify_existing, analyze"""
        try:
            prompt = f"""
Phân loại ý định của user dựa trên prompt sau:
"{request.prompt}"

Context (nếu có): {request.context_json}

Hãy xác định ý định là một trong các loại sau:
- CREATE_NEW: User muốn tạo code/function mới
- MODIFY_EXISTING: User muốn sửa/cải thiện code hiện có
- ANALYZE: User muốn phân tích/review code
- UNKNOWN: Không rõ ý định

Trả về CHÍNH XÁC format sau:
INTENT: <CREATE_NEW|MODIFY_EXISTING|ANALYZE|UNKNOWN>
CONFIDENCE: <0.0-1.0>
REASONING: <lý do>
"""
            
            response_text = self.gemini_repo.generate_code(prompt, model_name="gemini-2.5-flash")
            
            # Parse response
            intent_str = "UNKNOWN"
            confidence = 0.5
            reasoning = response_text
            
            if "CREATE_NEW" in response_text.upper():
                intent_str = "CREATE_NEW"
                confidence = 0.9
            elif "MODIFY" in response_text.upper():
                intent_str = "MODIFY_EXISTING"
                confidence = 0.85
            elif "ANALYZE" in response_text.upper():
                intent_str = "ANALYZE"
                confidence = 0.8
            
            return IntentClassifyResponse(
                intent=IntentType(intent_str.lower()),
                confidence=confidence,
                reasoning=reasoning,
                success=True
            )
            
        except Exception as e:
            return IntentClassifyResponse(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
                reasoning=str(e),
                success=False
            )
    
    # ==================== FLOW 3: ANALYZE CODE ====================
    
    def analyze_code(self, session_id: str) -> AgentResponse:
        """
        Luồng F3: Phân tích code vừa generate và tạo summary
        """
        try:
            session = self.session_repo.find_by_id(session_id)
            if not session or not session.code_history:
                return AgentResponse(
                    session_id=session_id,
                    current_step=WorkflowStep.ERROR.value,
                    success=False,
                    message="No code to analyze",
                    timestamp=datetime.now()
                )
            
            self.session_repo.update_step(session_id, WorkflowStep.ANALYZING_CODE)
            
            # Get latest code
            latest_code = session.code_history[-1]
            
            # Analyze with Gemini
            analysis_prompt = f"""
Phân tích code sau và tạo summary ngắn gọn:

```{latest_code['language']}
{latest_code['code']}
```

Hãy cung cấp:
1. Mô tả chức năng chính
2. Điểm mạnh
3. Điểm cần cải thiện (nếu có)
4. Complexity estimate
"""
            
            analysis = self.gemini_repo.generate_code(analysis_prompt, model_name="gemini-2.5-flash")
            
            session.current_step = WorkflowStep.COMPLETED
            self.session_repo.update(session)
            
            return AgentResponse(
                session_id=session_id,
                current_step=WorkflowStep.COMPLETED.value,
                code_analysis=analysis,
                success=True,
                message="Code analysis completed",
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.session_repo.update_step(session_id, WorkflowStep.ERROR)
            return AgentResponse(
                session_id=session_id,
                current_step=WorkflowStep.ERROR.value,
                success=False,
                message="Error analyzing code",
                error_message=str(e),
                timestamp=datetime.now()
            )

