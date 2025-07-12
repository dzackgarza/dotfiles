#!/usr/bin/env python3
"""
Bash Script Code Review Tool
Simple AI-powered code reviews for standalone bash scripts
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

class BashCodeReviewer:
    """Simple code reviewer for bash scripts"""
    
    BASE_URL = "https://api.groq.com/openai/v1"
    
    # Models that work well with bash script analysis
    PREFERRED_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
    ]
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_available_models(self) -> List[Dict]:
        """Fetch list of available models from Groq API"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/models",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def select_best_model(self, available_models: List[Dict]) -> Optional[str]:
        """Select the best model based on availability and preferences"""
        available_ids = {model["id"] for model in available_models}
        
        for preferred in self.PREFERRED_MODELS:
            if preferred in available_ids:
                return preferred
                
        # Fallback to first available model
        return available_models[0]["id"] if available_models else None
    
    def review_script(self, script_path: Path, model: str = None) -> str:
        """Review a bash script and provide feedback"""
        try:
            # Read the script content
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Get script stats
            line_count = len(script_content.splitlines())
            
            # Prepare the prompt
            prompt = f"""Please thoroughly review the following bash script and provide:
1. A brief summary of what the script does
2. Critical syntax errors (e.g., unclosed quotes, missing semicolons, incorrect syntax)
3. Logic errors (e.g., infinite loops, incorrect conditionals, improper variable usage)
4. Any potential security issues (e.g., unquoted variables, unsafe command substitutions)
5. Suggestions for improvement
6. Best practices that could be applied

For any issues found, please:
- Specify the line number(s) where the issue occurs
- Explain what's wrong
- Provide the corrected code if applicable

Script: {script_path.name}
Line count: {line_count}

```bash
{script_content}
```"""
            
            # Get available models if none specified
            if not model:
                available_models = self.get_available_models()
                model = self.select_best_model(available_models)
                if not model:
                    return "Error: No suitable model available"
            
            # Call the Groq API
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a senior bash script reviewer. Provide clear, concise feedback."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=30
            )
            response.raise_for_status()
            
            # Extract and return the response
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Error during script review: {str(e)}"

def load_api_key() -> Optional[str]:
    """Load Groq API key from environment or .env file"""
    # Try to load from .env file
    load_dotenv()
    
    # Check environment variables
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("Error: GROQ_API_KEY not found in environment variables or .env file")
        print("Please set the GROQ_API_KEY environment variable or create a .env file")
        return None
        
    return api_key

def main():
    """Main function"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Review a bash script using Groq AI')
    parser.add_argument('script', type=str, help='Path to the bash script to review')
    parser.add_argument('--model', type=str, help='Specific model to use (optional)')
    
    args = parser.parse_args()
    
    # Check if script exists
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script '{script_path}' not found")
        sys.exit(1)
    
    # Load API key
    api_key = load_api_key()
    if not api_key:
        sys.exit(1)
    
    # Create reviewer and get review
    reviewer = BashCodeReviewer(api_key)
    print(f"\n🔍 Reviewing {script_path.name}...\n")
    
    review = reviewer.review_script(script_path, args.model)
    print(review)

if __name__ == "__main__":
    main()
