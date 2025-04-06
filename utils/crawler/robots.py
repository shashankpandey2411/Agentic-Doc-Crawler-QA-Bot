import urllib.robotparser
import urllib.parse
import logging

class RobotsChecker:
    """Utility for checking robots.txt compliance."""
    
    def __init__(self):
        self.parsers = {}  # Cache for robot parsers
        
    def is_allowed(self, url, user_agent="*"):
        """Check if crawling a URL is allowed by robots.txt."""
        try:
            domain = urllib.parse.urlparse(url).netloc
            
            # Create parser for this domain if we don't have one
            if domain not in self.parsers:
                rp = urllib.robotparser.RobotFileParser()
                robots_url = f"{urllib.parse.urlparse(url).scheme}://{domain}/robots.txt"
                rp.set_url(robots_url)
                rp.read()
                self.parsers[domain] = rp
                
            # Check if URL is allowed
            return self.parsers[domain].can_fetch(user_agent, url)
            
        except Exception as e:
            logging.warning(f"Error checking robots.txt for {url}: {e}")
            # If there's an error, err on the side of caution and assume allowed
            return True 