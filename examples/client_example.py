#!/usr/bin/env python3
"""
Example client for AI Chat API
Demonstrates how to use the API for document upload and chat functionality
"""

import requests
import json
import time
from typing import Optional

class AIChatClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
    
    def upload_document(self, file_path: str) -> dict:
        """Upload a document to the API"""
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(f"{self.base_url}/documents/upload", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error uploading document: {e}")
            return {}
    
    def create_chat_session(self, session_name: str = "My Chat") -> str:
        """Create a new chat session"""
        try:
            data = {"session_name": session_name}
            response = requests.post(f"{self.base_url}/chat/sessions", json=data)
            response.raise_for_status()
            self.session_id = response.json()['id']
            return self.session_id
        except Exception as e:
            print(f"Error creating chat session: {e}")
            return ""
    
    def send_message(self, message: str) -> dict:
        """Send a message to the chat"""
        try:
            data = {
                "message": message,
                "session_id": self.session_id
            }
            response = requests.post(f"{self.base_url}/chat/send", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return {}
    
    def summarize_text(self, text: str, max_length: int = 100) -> str:
        """Summarize text using the API"""
        try:
            data = {
                "text": text,
                "max_length": max_length,
                "min_length": 30
            }
            response = requests.post(f"{self.base_url}/text/summarize", json=data)
            response.raise_for_status()
            return response.json()['summary']
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return ""
    
    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of text"""
        try:
            data = {"text": text}
            response = requests.post(f"{self.base_url}/text/sentiment", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {}
    
    def list_documents(self) -> list:
        """List all uploaded documents"""
        try:
            response = requests.get(f"{self.base_url}/documents/")
            response.raise_for_status()
            return response.json()['documents']
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []

def main():
    """Example usage of the AI Chat Client"""
    print("🤖 AI Chat API Client Example")
    print("=" * 40)
    
    # Initialize client
    client = AIChatClient()
    
    # Check if API is running
    if not client.health_check():
        print("❌ API is not running. Please start the server first.")
        print("Run: docker-compose up -d")
        return
    
    print("✅ API is running!")
    
    # Create a chat session
    print("\n📝 Creating chat session...")
    session_id = client.create_chat_session("Example Chat")
    if session_id:
        print(f"✅ Chat session created: {session_id}")
    
    # Example 1: Text summarization
    print("\n📄 Testing text summarization...")
    long_text = """
    Artificial Intelligence (AI) has become one of the most transformative technologies of our time. 
    It encompasses machine learning, deep learning, natural language processing, computer vision, 
    and many other subfields. AI systems can now perform tasks that were once thought to be 
    exclusively human, such as recognizing images, understanding speech, and even generating 
    creative content. The applications of AI are vast and growing, from healthcare and finance 
    to transportation and entertainment. However, with these advances come important considerations 
    about ethics, privacy, and the future of work. As we continue to develop more sophisticated 
    AI systems, it's crucial that we do so responsibly and with careful consideration of the 
    potential impacts on society.
    """
    
    summary = client.summarize_text(long_text, max_length=50)
    if summary:
        print(f"📝 Summary: {summary}")
    
    # Example 2: Sentiment analysis
    print("\n😊 Testing sentiment analysis...")
    test_texts = [
        "I love this new AI application! It's amazing!",
        "This is terrible. I hate it.",
        "The weather is okay today, nothing special."
    ]
    
    for text in test_texts:
        sentiment = client.analyze_sentiment(text)
        if sentiment:
            print(f"Text: '{text}'")
            print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']:.2f})")
            print()
    
    # Example 3: Chat functionality
    print("💬 Testing chat functionality...")
    chat_messages = [
        "Hello! How are you?",
        "What can you help me with?",
        "Can you tell me about artificial intelligence?"
    ]
    
    for message in chat_messages:
        print(f"👤 User: {message}")
        response = client.send_message(message)
        if response and 'message' in response:
            print(f"🤖 AI: {response['message']['content']}")
            if response.get('sources'):
                print(f"📚 Sources: {len(response['sources'])} relevant document chunks found")
        print()
    
    # Example 4: List documents
    print("📚 Listing uploaded documents...")
    documents = client.list_documents()
    if documents:
        print(f"Found {len(documents)} documents:")
        for doc in documents:
            print(f"  - {doc['filename']} ({doc['file_type']}, {doc['file_size']} bytes)")
    else:
        print("No documents uploaded yet.")
        print("💡 Tip: Upload documents using the /documents/upload endpoint to enable RAG chat!")
    
    print("\n✨ Example completed!")
    print("\n🔗 API Documentation available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
