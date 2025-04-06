import google.generativeai as genai
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiLLM:
    """Interface for interacting with Gemini LLM."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)
        
    def generate_answer(self, query: str, contexts: List[Dict[str, Any]], history=None):
        """Generate an answer based on query and retrieved contexts."""
        prompt = self._build_prompt(query, contexts)
        
        try:
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Post-process the response
            answer = self._post_process_response(response.text, contexts)
            return answer
            
        except Exception as e:
            logging.error(f"Error generating answer: {e}")
            return {
                "answer": "I encountered an error while generating your answer. Please try again.",
                "source_urls": [],
                "confidence": 0
            }
    
    def _build_prompt(self, query: str, contexts: List[Dict[str, Any]]):
        """Build a prompt for Gemini with context information."""
        context_text = "\n\n".join([
            f"Source {i+1} (from {ctx['metadata']['url']}):\n{ctx['page_content']}"
            for i, ctx in enumerate(contexts)
        ])
        
        prompt = f"""
        You are a helpful documentation assistant that provides accurate information based on the given documentation sources.
        
        [Documentation Sources]
        {context_text}
        
        [User Question]
        {query}
        
        Respond to the user's question based ONLY on the documentation sources provided above. 
        If the answer is not found in the documentation sources, state that you don't have that information.
        Include citations to source URLs when providing information.
        Format your response in a clear, well-structured manner.
        """
        return prompt
    
    def _post_process_response(self, response_text: str, contexts: List[Dict[str, Any]]):
        """Post-process the response to add metadata like sources."""
        # Extract unique source URLs from contexts
        source_urls = list(set([ctx['metadata']['url'] for ctx in contexts]))
        
        # Simplified confidence scoring based on response length and number of sources
        confidence = min(0.9, 0.5 + (len(response_text) / 1000) * 0.2 + len(source_urls) * 0.1)
        
        return {
            "answer": response_text,
            "source_urls": source_urls,
            "confidence": confidence
        } 