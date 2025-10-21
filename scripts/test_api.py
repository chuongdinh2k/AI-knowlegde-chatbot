#!/usr/bin/env python3
"""
Test script for AI Chat API
This script tests the main API endpoints
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_text_processing():
    """Test text processing endpoints"""
    print("\nTesting text processing...")
    
    # Test summarization
    try:
        summary_data = {
            "text": "This is a long text that needs to be summarized. It contains multiple sentences and should be reduced to a shorter version while maintaining the key information.",
            "max_length": 50,
            "min_length": 20
        }
        response = requests.post(f"{BASE_URL}/text/summarize", json=summary_data)
        if response.status_code == 200:
            print("✅ Text summarization works")
            print(f"Summary: {response.json()['summary']}")
        else:
            print(f"❌ Text summarization failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Text summarization error: {e}")
    
    # Test sentiment analysis
    try:
        sentiment_data = {
            "text": "I love this new AI application! It's amazing and works perfectly."
        }
        response = requests.post(f"{BASE_URL}/text/sentiment", json=sentiment_data)
        if response.status_code == 200:
            print("✅ Sentiment analysis works")
            print(f"Sentiment: {response.json()['sentiment']} (confidence: {response.json()['confidence']:.2f})")
        else:
            print(f"❌ Sentiment analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Sentiment analysis error: {e}")

def test_chat():
    """Test chat endpoints"""
    print("\nTesting chat functionality...")
    
    # Create a chat session
    try:
        session_data = {"session_name": "Test Chat"}
        response = requests.post(f"{BASE_URL}/chat/sessions", json=session_data)
        if response.status_code == 200:
            session_id = response.json()['id']
            print(f"✅ Chat session created: {session_id}")
            
            # Send a message
            message_data = {
                "message": "Hello, how are you?",
                "session_id": session_id
            }
            response = requests.post(f"{BASE_URL}/chat/send", json=message_data)
            if response.status_code == 200:
                print("✅ Chat message sent successfully")
                print(f"Response: {response.json()['message']['content']}")
            else:
                print(f"❌ Chat message failed: {response.status_code}")
        else:
            print(f"❌ Chat session creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat test error: {e}")

def test_documents():
    """Test document upload (requires actual file)"""
    print("\nTesting document functionality...")
    
    # List documents
    try:
        response = requests.get(f"{BASE_URL}/documents/")
        if response.status_code == 200:
            print("✅ Document listing works")
            print(f"Documents: {response.json()['total']}")
        else:
            print(f"❌ Document listing failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Document test error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting AI Chat API tests...")
    print(f"Testing against: {BASE_URL}")
    
    # Wait a bit for the server to start
    time.sleep(2)
    
    test_health()
    test_text_processing()
    test_chat()
    test_documents()
    
    print("\n✨ Tests completed!")

if __name__ == "__main__":
    main()
