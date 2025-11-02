"""
Quick test script - Test health endpoints
"""
import httpx
import asyncio


async def test_health():
    """Test all health endpoints"""
    base_url = "http://localhost:8080"
    
    endpoints = [
        "/health",
        "/api/ai/health",
        "/api/context/health",
        "/api/intent/health"
    ]
    
    async with httpx.AsyncClient() as client:
        print("\n" + "="*60)
        print("🏥 HEALTH CHECK TEST")
        print("="*60)
        
        for endpoint in endpoints:
            try:
                response = await client.get(f"{base_url}{endpoint}", timeout=5.0)
                if response.status_code == 200:
                    print(f"\n✅ {endpoint}")
                    print(f"   Response: {response.json()}")
                else:
                    print(f"\n❌ {endpoint}")
                    print(f"   Status: {response.status_code}")
            except Exception as e:
                print(f"\n❌ {endpoint}")
                print(f"   Error: {str(e)}")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    try:
        asyncio.run(test_health())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure the server is running: python app.py")
