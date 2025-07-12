"""
Simple test file for code review demonstration
"""

import time
import requests

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
    
    def fetch_data(self, endpoint):
        # TODO: Add error handling
        url = self.base_url + "/" + endpoint
        headers = {"Authorization": "Bearer " + self.api_key}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Process data
        results = []
        for item in data:
            if item["status"] == "active":
                results.append(item)
        
        return results
    
    def save_results(self, results, filename):
        # Save to file
        f = open(filename, "w")
        for result in results:
            f.write(str(result) + "\n")
        f.close()
        
        print("Saved " + str(len(results)) + " results")

# Usage
if __name__ == "__main__":
    fetcher = DataFetcher("secret-key-123")
    data = fetcher.fetch_data("users")
    fetcher.save_results(data, "output.txt")