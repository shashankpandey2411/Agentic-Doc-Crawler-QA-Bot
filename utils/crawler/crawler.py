import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from utils.error_handler import handle_request_error


class DocumentationCrawler:
    def __init__(self, base_url, max_pages=200, concurrency=5, crawl_delay=1):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.queue = [base_url]
        self.content_by_url = {}
        self.concurrency = concurrency
        self.crawl_delay = crawl_delay
        self.domain = urlparse(base_url).netloc
        
    def is_same_domain(self, url):
        """Check if URL belongs to the same domain."""
        return urlparse(url).netloc == self.domain
        
    def extract_links(self, soup, current_url):
        """Extract all links from a page that belong to the same domain."""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(current_url, href)
            
            # Filter URLs to keep only documentation pages
            if (self.is_same_domain(full_url) and 
                not full_url.endswith(('.png', '.jpg', '.pdf', '.zip', '.epub')) and
                '#' not in full_url and
                full_url not in self.visited_urls):
                links.append(full_url)
                
        return links
    
    def crawl_page(self, url):
        """Crawl a single page and return its content."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content = {
                'url': url,
                'title': soup.title.text if soup.title else url,
                'html': soup,
                'links': self.extract_links(soup, url)
            }
            
            time.sleep(self.crawl_delay)  # Respect robots.txt implicitly
            return url, content
            
        except Exception as e:
            handle_request_error(url, e)
            return url, None
    
    def crawl(self):
        """Crawl the documentation website starting from the base URL."""
        logging.info(f"Starting crawl from {self.base_url}")
        
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            while self.queue and len(self.visited_urls) < self.max_pages:
                # Get next batch of URLs to crawl
                batch = []
                while self.queue and len(batch) < self.concurrency:
                    url = self.queue.pop(0)
                    if url not in self.visited_urls:
                        batch.append(url)
                        self.visited_urls.add(url)
                
                if not batch:
                    break
                    
                # Crawl pages in parallel
                futures = [executor.submit(self.crawl_page, url) for url in batch]
                
                # Process results
                for future in futures:
                    url, content = future.result()
                    if content:
                        self.content_by_url[url] = content
                        # Add new links to the queue
                        for link in content['links']:
                            if link not in self.visited_urls and link not in self.queue:
                                self.queue.append(link)
        
        logging.info(f"Crawl complete. Processed {len(self.content_by_url)} pages.")
        return self.content_by_url 