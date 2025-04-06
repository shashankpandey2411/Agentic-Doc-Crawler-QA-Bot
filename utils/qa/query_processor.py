from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class QueryProcessor:
    """Process user queries to retrieve relevant documents."""
    
    def __init__(self, vector_store: Chroma, api_key: str, top_k=5):
        self.vector_store = vector_store
        self.api_key = api_key
        self.top_k = top_k
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )
        
    def process_query(self, query: str) -> List[Dict[str, Any]]:
        """Process a user query and retrieve relevant documents."""
        # Perform similarity search
        docs = self.vector_store.similarity_search_with_score(query, k=self.top_k)
        
        # Format results
        results = []
        for doc, score in docs:
            results.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
            
        return results 