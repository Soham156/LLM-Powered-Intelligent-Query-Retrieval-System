#!/usr/bin/env python3
"""
Test script for the LLM-Powered Query-Retrieval System
"""

import requests
import json
import sys
import os
from typing import Dict, Any

def test_api_endpoint():
    """Test the main API endpoint with sample data"""
    
    # Configuration
    BASE_URL = "http://localhost:8000"
    API_KEY = "f7d45b808bec922345421d7ed8051230ee8a696d8d37fe10e543bec6cf691c53"
    
    # Test data (using the provided sample)
    test_payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print("🚀 Testing LLM-Powered Query-Retrieval System")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False
    
    # Test main endpoint
    print("\n2. Testing main query endpoint...")
    print(f"Document URL: {test_payload['documents'][:80]}...")
    print(f"Number of questions: {len(test_payload['questions'])}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/hackrx/run",
            headers=headers,
            json=test_payload,
            timeout=120  # Allow up to 2 minutes for processing
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Query processing successful")
            print(f"Number of answers received: {len(result.get('answers', []))}")
            
            # Display results
            print("\n📋 Results:")
            print("-" * 60)
            for i, (question, answer) in enumerate(zip(test_payload['questions'], result.get('answers', [])), 1):
                print(f"\n🔍 Question {i}:")
                print(f"Q: {question}")
                print(f"A: {answer[:200]}{'...' if len(answer) > 200 else ''}")
            
            return True
            
        else:
            print(f"❌ Query processing failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Query processing error: {str(e)}")
        return False

def test_authentication():
    """Test authentication with invalid token"""
    print("\n3. Testing authentication...")
    
    BASE_URL = "http://localhost:8000"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer invalid_token"
    }
    
    test_payload = {
        "documents": "https://example.com/test.pdf",
        "questions": ["Test question"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/hackrx/run",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Authentication test passed (correctly rejected invalid token)")
            return True
        else:
            print(f"❌ Authentication test failed: Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting API Tests")
    
    # Check if environment is set up
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some tests may fail.")
    
    # Run tests
    tests = [
        test_api_endpoint,
        test_authentication
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the logs and configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
