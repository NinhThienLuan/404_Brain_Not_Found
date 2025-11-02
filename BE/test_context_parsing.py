"""
Test Context Parsing Service

Kiểm tra service trích xuất context từ user input
"""

import asyncio
import json
from service.context_parsing_service import ContextParsingService


async def test_context_parsing():
    """Test basic context parsing"""
    
    print("=" * 60)
    print("🧪 TEST CONTEXT PARSING SERVICE")
    print("=" * 60)
    
    # Initialize service
    service = ContextParsingService()
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Function",
            "context": "Tạo hàm tính tổng hai số a và b, trả về kết quả"
        },
        {
            "name": "Data Processing",
            "context": "Viết function đọc file CSV, lọc các dòng có giá trị > 100, và lưu kết quả ra file mới"
        },
        {
            "name": "API Endpoint",
            "context": "Tạo API endpoint nhận username và password, kiểm tra trong database, trả về JWT token nếu đúng"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 60}")
        print(f"Test {i}: {test['name']}")
        print(f"{'─' * 60}")
        print(f"📝 Input: {test['context']}\n")
        
        # Extract context - use default model
        success, parsed_context, error = service.extract_one_shot(
            test['context']
        )
        
        if success and parsed_context:
            print("✅ SUCCESS!")
            print(f"\n📊 Parsed Context:")
            print(f"  - Goal Type: {parsed_context.goal_type}")
            
            func_details = parsed_context.get_function_details()
            if func_details:
                print(f"  - Function Name: {func_details.function_name}")
                print(f"  - Purpose: {func_details.purpose}")
                print(f"  - Inputs: {len(func_details.inputs)} parameters")
                for inp in func_details.inputs:
                    print(f"    • {inp.name} ({inp.type}): {inp.description}")
                print(f"  - Core Logic Steps: {len(func_details.core_logic)}")
                for j, step in enumerate(func_details.core_logic, 1):
                    print(f"    {j}. {step}")
                if func_details.outputs:
                    print(f"  - Output Type: {func_details.outputs.type}")
                    print(f"  - Output Description: {func_details.outputs.description}")
        else:
            print(f"❌ FAILED: {error}")
    
    print(f"\n{'=' * 60}")
    print("✨ Test completed!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(test_context_parsing())
