import requests

class URLResolver:
    def __init__(self, timeout=10):
        self.timeout = timeout
        
    def resolve_bitly(self, url):
        """Resolve a bit.ly URL to its target URL."""
        try:
            response = requests.head(url, 
                                    allow_redirects=True, 
                                    timeout=self.timeout)
            return response.url
        except requests.RequestException as e:
            raise ValueError(f"Failed to resolve URL: {e}")
    
    def fetch_content(self, url):
        """Fetch content from the URL."""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch content: {e}")
