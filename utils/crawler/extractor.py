from bs4 import BeautifulSoup
import re
import logging

class ContentExtractor:
    """Extract meaningful content from HTML documents while filtering out navigation, 
    headers, footers, and other non-content elements."""
    
    def __init__(self):
        # Common class and ID patterns for non-content elements
        self.noise_patterns = [
            'nav', 'navigation', 'menu', 'footer', 'header', 'sidebar', 
            'comment', 'advertisement', 'ad-', 'cookie', 'popup', 'banner',
            'promo', 'dialog'
        ]
    
    def is_noise_element(self, element):
        """Check if an element is likely to be non-content."""
        if not element.name:
            return False
            
        # Check element's class and id attributes
        for attr in ['class', 'id']:
            if element.has_attr(attr):
                attr_value = ' '.join(element[attr]) if isinstance(element[attr], list) else element[attr]
                for pattern in self.noise_patterns:
                    if pattern in attr_value.lower():
                        return True
        return False
    
    def extract_content(self, html_content):
        """Extract clean content from HTML."""
        soup = html_content if isinstance(html_content, BeautifulSoup) else BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'iframe', 'noscript']):
            element.decompose()
            
        # Try to identify main content area
        main_content = None
        for tag in ['main', 'article', 'div[role="main"]', '.content', '.main-content', '#content', '#main']:
            if tag.startswith('.'):
                elements = soup.select(tag[1:])
            elif tag.startswith('#'):
                elements = soup.select(tag)
            else:
                elements = soup.find_all(tag)
                
            if elements:
                # Use the largest element as it's likely the main content
                main_content = max(elements, key=lambda x: len(str(x)))
                break
        
        # If no main content found, use body
        if not main_content:
            main_content = soup.body if soup.body else soup
            
        # Remove noise elements from the main content
        for element in list(main_content.find_all()):
            if self.is_noise_element(element):
                element.decompose()
                
        # Extract structured content
        extracted = {
            'title': soup.title.text if soup.title else "",
            'headings': self._extract_headings(main_content),
            'paragraphs': self._extract_paragraphs(main_content),
            'lists': self._extract_lists(main_content),
            'tables': self._extract_tables(main_content),
            'full_text': main_content.get_text(separator=' ', strip=True)
        }
        
        return extracted
    
    def _extract_headings(self, content):
        """Extract headings with their hierarchy."""
        headings = []
        for level in range(1, 7):
            for h in content.find_all(f'h{level}'):
                headings.append({
                    'level': level,
                    'text': h.get_text(strip=True)
                })
        return headings
    
    def _extract_paragraphs(self, content):
        """Extract paragraphs."""
        return [p.get_text(strip=True) for p in content.find_all('p') if p.get_text(strip=True)]
    
    def _extract_lists(self, content):
        """Extract lists."""
        lists = []
        for list_tag in content.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in list_tag.find_all('li')]
            lists.append({
                'type': list_tag.name,
                'items': items
            })
        return lists
    
    def _extract_tables(self, content):
        """Extract tables."""
        tables = []
        for table in content.find_all('table'):
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text(strip=True))
            
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if cells:
                    rows.append(cells)
                    
            tables.append({
                'headers': headers,
                'rows': rows
            })
        return tables 