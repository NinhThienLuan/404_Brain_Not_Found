from BE.service.code_generation_service import CodeGenerationService


def main():
    svc = CodeGenerationService()

    mock_requirement = {
        "request_id": "req_test_001",
        "language": "python",
        "task": "Viết hàm tính giai thừa n! theo iterative và có docstring",
        "constraints": {"max_lines": 80, "style": "clear and documented"},
        "examples": [{"input": 5, "output": 120}]
    }

    out = svc.generate_from_requirement(mock_requirement)

    print("=== PROMPT ===")
    print(out.get("prompt"))
    print("\n=== RESPONSE ===")
    print(out.get("response"))

    # --- Now test generation from raw user context using ContextParsingService ---
    print("\n--- Test: generate_from_user_context ---")
    user_context = (
        "Tôi cần một hàm tên factorial nhận vào n (int) trả về n!; nên có docstring và kiểm tra đầu vào."
    )

    out2 = svc.generate_from_user_context(user_context)
    print("result:", out2)


if __name__ == "__main__":
    main()
