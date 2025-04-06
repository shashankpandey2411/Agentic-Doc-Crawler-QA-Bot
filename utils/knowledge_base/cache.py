import os
import json
import hashlib
from datetime import datetime, timedelta

class Cache:
    """Cache system for storing crawled websites and queries."""
    
    def __init__(self, cache_dir="./cache", expiry_days=7):
        self.cache_dir = cache_dir
        self.expiry_days = expiry_days
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
    def _get_key(self, data):
        """Generate a unique key for data."""
        if isinstance(data, str):
            return hashlib.md5(data.encode()).hexdigest()
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def get(self, key_data):
        """Get data from cache if it exists and hasn't expired."""
        key = self._get_key(key_data)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if not os.path.exists(cache_file):
            return None
            
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                
            # Check if cache has expired
            stored_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - stored_time > timedelta(days=self.expiry_days):
                os.remove(cache_file)  # Delete expired cache
                return None
                
            return cached_data['data']
            
        except Exception as e:
            print(f"Cache error: {e}")
            return None
    
    def set(self, key_data, value):
        """Store data in cache."""
        key = self._get_key(key_data)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        cache_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': value
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_entry, f)
            return True
        except Exception as e:
            print(f"Cache write error: {e}")
            return False 