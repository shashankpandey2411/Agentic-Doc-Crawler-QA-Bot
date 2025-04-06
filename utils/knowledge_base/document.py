from typing import List, Optional
import uuid

class DocSection:
    """Represents a section of documentation with hierarchical structure."""
    
    def __init__(self, doc_id: str, section_id: str, heading: str, content: str, 
                 url: str, level: int = 0, parent=None):
        self.doc_id = doc_id
        self.section_id = section_id
        self.heading = heading
        self.content = content
        self.url = url
        self.level = level
        self.parent = parent
        self.children: List['DocSection'] = []
        
    def add_child(self, child: 'DocSection'):
        """Add a child section."""
        child.parent = self
        self.children.append(child)
        
    def flatten(self) -> List['DocSection']:
        """Convert hierarchical structure to flat list."""
        result = [self]
        for child in self.children:
            result.extend(child.flatten())
        return result
    
    def get_full_path(self) -> str:
        """Get the full hierarchical path to this section."""
        if self.parent and self.parent.heading:
            return f"{self.parent.get_full_path()} > {self.heading}"
        return self.heading 