from openai import OpenAI
from langchain.llms import OpenAI as LangChainOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.chat_model = ChatOpenAI(
            openai_api_key=settings.openai_api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """Generate a response using OpenAI GPT"""
        try:
            messages = []
            
            if context:
                system_message = f"""You are a helpful AI assistant. Use the following context to answer the user's question. 
                If the context doesn't contain relevant information, say so and provide a general helpful response.
                
                Context: {context}"""
                messages.append(SystemMessage(content=system_message))
            
            messages.append(HumanMessage(content=message))
            
            response = self.chat_model(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """Summarize text using OpenAI"""
        try:
            prompt = f"""Please summarize the following text in {max_length} words or less, but at least {min_length} words. 
            Focus on the main points and key information:
            
            {text}"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_length * 2,  # Allow some buffer
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            raise
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using OpenAI"""
        try:
            prompt = f"""Analyze the sentiment of the following text. Respond with a JSON object containing:
            - sentiment: "positive", "negative", or "neutral"
            - confidence: a float between 0 and 1
            - scores: an object with "positive", "negative", "neutral" scores
            
            Text: {text}"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # Parse JSON response
            import json
            result = json.loads(response.choices[0].message.content.strip())
            return result
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            # Fallback to simple sentiment analysis
            return self._simple_sentiment_analysis(text)
    
    def _simple_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Simple fallback sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'joy']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'disappointed']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.8, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": {
                "positive": positive_count / len(text.split()),
                "negative": negative_count / len(text.split()),
                "neutral": 1 - (positive_count + negative_count) / len(text.split())
            }
        }
    
    def create_retrieval_qa_chain(self, vectorstore):
        """Create a retrieval QA chain for document-based questions"""
        try:
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.chat_model,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            
            return qa_chain
        except Exception as e:
            logger.error(f"Error creating QA chain: {e}")
            raise

# Global instance
llm_service = LLMService()
