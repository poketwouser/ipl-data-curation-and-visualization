# utils/caching.py
import pandas as pd
import pickle
import os
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cached_data(self, key, max_age_hours=24):
        """Get cached data if it exists and is not expired"""
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        
        if not os.path.exists(cache_file):
            return None
        
        # Check if cache is expired
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - file_time > timedelta(hours=max_age_hours):
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def set_cached_data(self, key, data):
        """Store data in cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            return True
        except:
            return False
    
    def clear_cache(self, key=None):
        """Clear cache for specific key or all cache"""
        if key:
            cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
            if os.path.exists(cache_file):
                os.remove(cache_file)
        else:
            for file in os.listdir(self.cache_dir):
                if file.endswith('.pkl'):
                    os.remove(os.path.join(self.cache_dir, file))

# Global cache instance
data_cache = DataCache()