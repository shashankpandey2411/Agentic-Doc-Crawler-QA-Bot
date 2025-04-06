import uuid
from typing import List, Dict, Any
import logging
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.knowledge_base.document import DocSection

class DocumentProcessor:
    def __init__(self, api_key: str, chunk_size=1000, chunk_overlap=200):
        self.api_key = api_key
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )
        
    def create_documents(self, extracted_contents: Dict[str, Dict[str, Any]]) -> List[Document]:
        """Convert extracted content into LangChain documents."""
        documents = []
        
        for url, content in extracted_contents.items():
            # Skip if content extraction failed
            if not content or not content.get('html'):
                continue
                
            extracted = content.get('extracted', {})
            if not extracted:
                # Extract content if not already done
                from ..crawler.extractor import ContentExtractor
                extractor = ContentExtractor()
                extracted = extractor.extract_content(content['html'])
                content['extracted'] = extracted
            
            # Process each section as a separate document
            
            # Add title and headings
            title = extracted.get('title', '')
            doc_id = str(uuid.uuid4())
            
            # Create a document structure maintaining the hierarchy
            doc_structure = self._create_document_structure(extracted, url, title, doc_id)
            
            # Convert to flat documents for vector storage
            for section in doc_structure.flatten():
                doc = Document(
                    page_content=section.content,
                    metadata={
                        "url": url,
                        "title": title,
                        "section": section.heading,
                        "doc_id": doc_id,
                        "section_id": section.section_id
                    }
                )
                documents.append(doc)
            
        return documents
    
    def _create_document_structure(self, extracted, url, title, doc_id):
        """Create a hierarchical document structure."""
        root = DocSection(doc_id=doc_id, section_id="root", heading=title, content=title, url=url)
        
        # Sort headings by level and position
        headings = sorted(extracted.get('headings', []), key=lambda h: (h['level'], extracted['headings'].index(h)))
        
        # Current section stack to track hierarchy
        section_stack = [root]
        
        # Process each heading as a section
        for i, heading in enumerate(headings):
            level = heading['level']
            text = heading['text']
            
            # Pop stack until we're at the right level
            while len(section_stack) > 1 and section_stack[-1].level >= level:
                section_stack.pop()
                
            # Create new section
            parent = section_stack[-1]
            section_id = f"{doc_id}_{i}"
            
            # Get content between this heading and the next
            content = self._get_section_content(extracted, headings, i)
            
            # Create new section
            new_section = DocSection(
                doc_id=doc_id,
                section_id=section_id,
                heading=text,
                content=f"{text}\n\n{content}",
                url=url,
                level=level
            )
            
            # Add to parent and push to stack
            parent.add_child(new_section)
            section_stack.append(new_section)
            
        return root
    
    def _get_section_content(self, extracted, headings, heading_index):
        """Extract content that belongs to a specific heading."""
        # This is simplified - a real implementation would need to map
        # content to the correct heading based on position in the document
        paragraphs = extracted.get('paragraphs', [])
        
        # For illustration, we'll just return some paragraphs
        # A real implementation would be more sophisticated
        return "\n\n".join(paragraphs[heading_index:heading_index+3 if heading_index+3 < len(paragraphs) else len(paragraphs)])
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks."""
        return self.text_splitter.split_documents(documents)
    
    def create_vector_store(self, documents: List[Document], persist_directory="./chroma_db"):
        """Create and persist vector store from documents."""
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        vector_store.persist()
        logging.info(f"Vector store created with {len(documents)} chunks")
        return vector_store 