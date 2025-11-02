"""
🎬 DEMO - AI Function 200 Project
Showcase tất cả chức năng của hệ thống
"""

import asyncio
import json
import httpx
from typing import Dict, Any


class AIFunction200Demo:
    """Demo class cho tất cả chức năng"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.api_prefix = "/api"
        
    def print_header(self, title: str):
        """Print section header"""
        print("\n" + "=" * 80)
        print(f"🎯 {title}")
        print("=" * 80)
    
    def print_result(self, result: Dict[Any, Any], title: str = "Result"):
        """Print formatted result"""
        print(f"\n✨ {title}:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    async def test_health_check(self):
        """Test 0: Health Check"""
        self.print_header("TEST 0: Health Check")
        
        async with httpx.AsyncClient() as client:
            # Root health check
            response = await client.get(f"{self.base_url}/health")
            print(f"✅ Root Health: {response.status_code}")
            self.print_result(response.json(), "Root Health")
            
            # AI Service health
            response = await client.get(f"{self.base_url}{self.api_prefix}/ai/health")
            print(f"✅ AI Service Health: {response.status_code}")
            self.print_result(response.json(), "AI Service Health")
            
            # Context Service health
            response = await client.get(f"{self.base_url}{self.api_prefix}/context/health")
            print(f"✅ Context Service Health: {response.status_code}")
            self.print_result(response.json(), "Context Service Health")
            
            # Intent Service health
            response = await client.get(f"{self.base_url}{self.api_prefix}/intent/health")
            print(f"✅ Intent Service Health: {response.status_code}")
            self.print_result(response.json(), "Intent Service Health")
    
    async def test_context_parsing(self):
        """Test 1: Context Parsing Service"""
        self.print_header("TEST 1: Context Parsing Service (Service 1)")
        print("📝 Chức năng: Trích xuất context từ user input thành JSON structure")
        
        test_cases = [
            {
                "name": "Simple Function",
                "user_context": "Tạo hàm tính tổng hai số a và b, trả về kết quả"
            },
            {
                "name": "Authentication Function",
                "user_context": "Viết function login, nhận username và password, kiểm tra trong database, trả về JWT token nếu đúng"
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, test in enumerate(test_cases, 1):
                print(f"\n{'─' * 80}")
                print(f"📋 Test Case {i}: {test['name']}")
                print(f"Input: {test['user_context']}")
                
                response = await client.post(
                    f"{self.base_url}{self.api_prefix}/context/parse",
                    json={
                        "user_context": test["user_context"],
                        "model": "gemini-2.5-flash"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print("✅ SUCCESS!")
                        parsed = result.get("parsed_context", {})
                        details = parsed.get("details", {})
                        print(f"  - Function Name: {details.get('function_name')}")
                        print(f"  - Purpose: {details.get('purpose')}")
                        print(f"  - Inputs: {len(details.get('inputs', []))} parameters")
                        print(f"  - Core Logic Steps: {len(details.get('core_logic', []))}")
                    else:
                        print(f"❌ FAILED: {result.get('error')}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
    
    async def test_intent_classification(self):
        """Test 2: Intent Classification Service"""
        self.print_header("TEST 2: Intent Classification Service")
        print("📝 Chức năng: Phân loại ý định của user (NEW vs REFINE)")
        
        test_cases = [
            {
                "name": "New Request",
                "user_message": "Tôi muốn tạo một hàm tính giai thừa",
                "session_id": "session_001"
            },
            {
                "name": "Refinement Request",
                "user_message": "Thêm error handling cho trường hợp n < 0",
                "session_id": "session_002"
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, test in enumerate(test_cases, 1):
                print(f"\n{'─' * 80}")
                print(f"📋 Test Case {i}: {test['name']}")
                print(f"Message: {test['user_message']}")
                
                response = await client.post(
                    f"{self.base_url}{self.api_prefix}/intent/classify",
                    json={
                        "user_message": test["user_message"],
                        "session_id": test["session_id"]
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Intent: {result.get('intent')}")
                    print(f"  - Session ID: {result.get('session_id')}")
                    if result.get('next_question'):
                        print(f"  - Next Question: {result.get('next_question')}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
    
    async def test_code_generation(self):
        """Test 3: Code Generation Service"""
        self.print_header("TEST 3: Code Generation Service")
        print("📝 Chức năng: Generate code từ prompt")
        
        test_cases = [
            {
                "name": "Fibonacci Function",
                "prompt": "Create a Python function to calculate fibonacci sequence with memoization",
                "language": "python"
            },
            {
                "name": "FastAPI Endpoint",
                "prompt": "Create a FastAPI POST endpoint to register a new user",
                "language": "python",
                "framework": "fastapi"
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, test in enumerate(test_cases, 1):
                print(f"\n{'─' * 80}")
                print(f"📋 Test Case {i}: {test['name']}")
                print(f"Prompt: {test['prompt']}")
                
                payload = {
                    "prompt": test["prompt"],
                    "language": test["language"],
                    "model": "gemini-2.5-flash"
                }
                
                if "framework" in test:
                    payload["framework"] = test["framework"]
                
                response = await client.post(
                    f"{self.base_url}{self.api_prefix}/ai/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print("✅ SUCCESS!")
                        print(f"\n📄 Generated Code:\n")
                        print(result.get("generated_code", "")[:300] + "...")
                        print(f"\n📝 Explanation: {result.get('explanation', '')[:200]}...")
                    else:
                        print(f"❌ FAILED: {result.get('error_message')}")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
    
    async def test_code_review(self):
        """Test 4: Code Review Service"""
        self.print_header("TEST 4: Code Review Service")
        print("📝 Chức năng: Review code và đưa ra suggestions")
        
        code_sample = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        
        print(f"📄 Code to review:\n{code_sample}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}{self.api_prefix}/ai/review",
                json={
                    "code": code_sample,
                    "language": "python",
                    "review_type": "performance",
                    "model": "gemini-2.5-flash"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print("✅ SUCCESS!")
                    print(f"\n⭐ Overall Score: {result.get('overall_score')}/10")
                    print(f"\n📊 Issues Found: {len(result.get('issues', []))}")
                    
                    for issue in result.get('issues', [])[:3]:  # Show first 3
                        print(f"\n  - Severity: {issue.get('severity')}")
                        print(f"    Type: {issue.get('issue_type')}")
                        print(f"    Description: {issue.get('description')}")
                        print(f"    Suggestion: {issue.get('suggestion')}")
                    
                    print(f"\n📝 Summary:\n{result.get('summary', '')[:200]}...")
                else:
                    print(f"❌ FAILED: {result.get('error_message')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
    
    async def test_end_to_end_workflow(self):
        """Test 5: End-to-End Workflow"""
        self.print_header("TEST 5: End-to-End Workflow (Complete Flow)")
        print("📝 Workflow: Context Parse → Intent Classify → Code Generate → Code Review")
        
        session_id = "demo_session_e2e"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Step 1: Parse Context
            print("\n🔹 Step 1: Parse User Context")
            user_context = "Tạo API endpoint để update thông tin user, nhận user_id và data mới, validate data, update vào database"
            
            context_response = await client.post(
                f"{self.base_url}{self.api_prefix}/context/parse",
                json={
                    "user_context": user_context,
                    "model": "gemini-2.5-flash"
                }
            )
            
            if context_response.status_code == 200:
                context_result = context_response.json()
                if context_result.get("success"):
                    print("✅ Context parsed successfully")
                    parsed = context_result.get("parsed_context", {})
                    details = parsed.get("details", {})
                    print(f"  Function: {details.get('function_name')}")
                    print(f"  Purpose: {details.get('purpose')}")
                else:
                    print(f"❌ Context parsing failed")
                    return
            
            # Step 2: Classify Intent
            print("\n🔹 Step 2: Classify User Intent")
            intent_response = await client.post(
                f"{self.base_url}{self.api_prefix}/intent/classify",
                json={
                    "user_message": user_context,
                    "session_id": session_id
                }
            )
            
            if intent_response.status_code == 200:
                intent_result = intent_response.json()
                print(f"✅ Intent classified: {intent_result.get('intent')}")
            
            # Step 3: Generate Code
            print("\n🔹 Step 3: Generate Code")
            gen_response = await client.post(
                f"{self.base_url}{self.api_prefix}/ai/generate",
                json={
                    "prompt": f"{details.get('purpose')}. Function name: {details.get('function_name')}",
                    "language": "python",
                    "framework": "fastapi",
                    "model": "gemini-2.5-flash"
                }
            )
            
            generated_code = ""
            if gen_response.status_code == 200:
                gen_result = gen_response.json()
                if gen_result.get("success"):
                    print("✅ Code generated successfully")
                    generated_code = gen_result.get("generated_code", "")
                    print(f"\n📄 Preview:\n{generated_code[:200]}...")
            
            # Step 4: Review Generated Code
            if generated_code:
                print("\n🔹 Step 4: Review Generated Code")
                review_response = await client.post(
                    f"{self.base_url}{self.api_prefix}/ai/review",
                    json={
                        "code": generated_code,
                        "language": "python",
                        "review_type": "general",
                        "model": "gemini-2.5-flash"
                    }
                )
                
                if review_response.status_code == 200:
                    review_result = review_response.json()
                    if review_result.get("success"):
                        print("✅ Code reviewed successfully")
                        print(f"  Score: {review_result.get('overall_score')}/10")
                        print(f"  Issues: {len(review_result.get('issues', []))}")
            
            print("\n🎉 End-to-End Workflow Completed!")
    
    async def run_all_tests(self):
        """Run all demo tests"""
        print("\n" + "🎬" * 40)
        print("🎬 AI FUNCTION 200 - COMPLETE DEMO")
        print("🎬" * 40)
        
        try:
            await self.test_health_check()
            await asyncio.sleep(1)
            
            await self.test_context_parsing()
            await asyncio.sleep(1)
            
            await self.test_intent_classification()
            await asyncio.sleep(1)
            
            await self.test_code_generation()
            await asyncio.sleep(1)
            
            await self.test_code_review()
            await asyncio.sleep(1)
            
            await self.test_end_to_end_workflow()
            
            print("\n" + "🎉" * 40)
            print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
            print("🎉" * 40)
            
        except Exception as e:
            print(f"\n❌ Demo Error: {str(e)}")
            print("💡 Make sure the server is running: python app.py")


async def main():
    """Main entry point"""
    demo = AIFunction200Demo()
    await demo.run_all_tests()


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                     🤖 AI FUNCTION 200 - DEMO SUITE 🤖                     ║
║                                                                            ║
║  This demo showcases all features of the AI Function 200 system:          ║
║                                                                            ║
║  ✅ Context Parsing Service - Extract structured info from user input     ║
║  ✅ Intent Classification - Classify user intent (NEW/REFINE/CHITCHAT)    ║
║  ✅ Code Generation - Generate code from prompts                          ║
║  ✅ Code Review - Review and suggest improvements                         ║
║  ✅ End-to-End Workflow - Complete flow demonstration                     ║
║                                                                            ║
║  📋 Requirements:                                                          ║
║  - Server must be running on http://localhost:8080                        ║
║  - Run: python app.py (in another terminal)                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n⏳ Starting demo in 3 seconds...")
    import time
    time.sleep(3)
    
    asyncio.run(main())
