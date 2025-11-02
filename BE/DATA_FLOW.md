# Luồng dữ liệu - Agent Orchestration → Context Parsing → Code Generation

## Tóm tắt luồng chính (process_context)

```
User Request (context_text, model)
    ↓
AgentOrchestrationService.process_context(session_id, context_text, model)
    ↓
ContextParsingService.extract_one_shot(context_text, model_name=model)
    ↓ (gọi Gemini để parse)
GeminiRepository.generate_code(prompt, model_name=model_name)
    ↓ (trả về JSON)
ParsedContextV2 (goal_type, details: {function_name, purpose, inputs, core_logic, outputs})
    ↓
AgentOrchestrationService xây dựng prompt từ parsed context
    ↓
CodeGenerationRequest(prompt, language="python", additional_context, model)
    ↓
CodeGenerationService.generate_code(request)
    ↓ (gọi Gemini để gen code)
GeminiRepository.generate_code(prompt, model_name=request.model)
    ↓
CodeGenerationResponse (generated_code, explanation, success)
    ↓
Lưu vào session.code_history
    ↓
AgentResponse (generated_code, context_json, success)
```

## Chi tiết từng bước

### 1. AgentOrchestrationService.process_context

**Input**:
- `session_id`: str
- `context_text`: str (yêu cầu từ user)
- `model`: str (default="gemini-2.5-flash")

**Xử lý**:
1. Update session step → `PARSING_CONTEXT`
2. Gọi `context_parsing_service.extract_one_shot(context_text, model_name=model)`
3. Nhận kết quả `(ok, parsed_ctx, err)`
4. Convert `parsed_ctx` → `parsed_json` (dict) và lưu vào session
5. Xây dựng prompt từ `parsed_json["details"]`:
   - Goal type
   - Purpose
   - Function name
   - Inputs (list)
   - Core logic (list)
   - Outputs (dict)
6. Tạo `CodeGenerationRequest` với:
   - `prompt`: prompt đã build
   - `language`: "python"
   - `additional_context`: str(session.context_json)
   - `model`: model parameter gốc
7. Gọi `code_gen_service.generate_code(code_request)`
8. Xử lý response và lưu vào `session.code_history`

**Output**:
- `AgentResponse` với `generated_code`, `context_json`, `success`

### 2. ContextParsingService.extract_one_shot

**Input**:
- `user_context`: str
- `model_name`: Optional[str]

**Xử lý**:
1. Build extraction prompt từ template (yêu cầu Gemini trả về JSON với structure: function_name, purpose, inputs, core_logic, outputs)
2. Gọi `gemini_repo.generate_code(prompt, model_name=model_name)`
3. Parse JSON response
4. Convert sang `ParsedContextV2`:
   - `goal_type`: GoalType.GENERATE_FUNCTION
   - `details`: dict với function_name, purpose, inputs, core_logic, outputs, error_handling

**Output**:
- Tuple `(ok: bool, parsed_ctx: ParsedContextV2, err: Optional[str])`

### 3. CodeGenerationService.generate_code

**Input**:
- `request`: CodeGenerationRequest
  - `prompt`: str
  - `language`: str
  - `framework`: Optional[str]
  - `additional_context`: Optional[str]
  - `model`: str

**Xử lý**:
1. Build generation prompt từ request:
   ```
   Generate {language} code for the following requirement:
   {prompt}
   
   [Framework if specified]
   [Additional context if provided]
   
   Please provide:
   1. Clean, well-structured code
   2. Comments explaining key parts
   3. Brief explanation of the implementation
   ```
2. Gọi `gemini_repo.generate_code(prompt, model_name=request.model)`
3. Parse response để extract code block (```...```) và explanation

**Output**:
- `CodeGenerationResponse`:
  - `generated_code`: str
  - `explanation`: str
  - `language`: str
  - `success`: bool
  - `error_message`: Optional[str]

## Parameter Flow Check ✅

| Step | Parameter | Source | Destination | Status |
|------|-----------|--------|-------------|--------|
| 1 | `model` | User/API → process_context | `model_name` in extract_one_shot | ✅ Correct |
| 2 | `model_name` | extract_one_shot | GeminiRepo.generate_code | ✅ Correct |
| 3 | `model` | process_context | CodeGenerationRequest.model | ✅ Correct |
| 4 | `request.model` | CodeGenerationRequest | GeminiRepo.generate_code | ✅ Correct |
| 5 | `context_text` | User → process_context | extract_one_shot | ✅ Correct |
| 6 | `parsed_json` | ParsedContextV2 → dict | Build prompt | ✅ Correct |
| 7 | `prompt` | Built from parsed_json | CodeGenerationRequest | ✅ Correct |

## Vấn đề đã fix

### 1. Import sai trong ai_service.py
**Trước**:
```python
from model.ai_models import (  # ❌ Thiếu BE.
```

**Sau**:
```python
from BE.model.ai_models import (  # ✅ Đúng
```

## Notes

- Tất cả parameter được forward đúng qua các tầng
- `model` parameter được truyền nhất quán từ API → GeminiRepository
- Context được parse thành structured JSON trước khi gen code
- Prompt được build chi tiết từ parsed context (function_name, purpose, inputs, logic, outputs)
- Response được parse để extract code block và explanation
- Session history được update sau mỗi code generation

## Testing

Chạy test với mock để verify flow:
```powershell
$env:PYTHONPATH='D:\Semester5\HACKATHON\404_Brain_Not_Found'
python BE/test_all_features.py
```
