#!/usr/bin/python3
"""
Groq Code Review Tool
Sends files to Groq API for AI-powered code review using the latest models.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
from datetime import datetime


class GroqCodeReviewer:
    """Handles Groq API interactions for code review."""
    
    BASE_URL = "https://api.groq.com/openai/v1"
    
    # Model preferences based on July 2025 capabilities
    # Prioritize newer models with better code understanding
    PREFERRED_MODELS = [
        "llama-3.3-70b-versatile",  # Latest Llama with strong code capabilities
        "mixtral-8x7b-32768",       # Good for code with large context
        "llama3-70b-8192",          # Strong general model
        "gemma2-9b-it",             # Good for detailed analysis
        "llama3-8b-8192",           # Fallback smaller model
    ]
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def get_available_models(self) -> List[Dict]:
        """Fetch list of available models from Groq API."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/models",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def select_best_model(self, available_models: List[Dict]) -> Optional[str]:
        """Select the best model based on availability and preferences."""
        available_ids = {model["id"] for model in available_models}
        
        # Try preferred models in order
        for preferred in self.PREFERRED_MODELS:
            if preferred in available_ids:
                return preferred
                
        # Fallback to any available model with "llama" or "mixtral" in name
        for model in available_models:
            model_id = model["id"].lower()
            if "llama" in model_id or "mixtral" in model_id:
                return model["id"]
                
        # Last resort - use first available
        return available_models[0]["id"] if available_models else None
    
    def review_code(self, file_path: Path, model: str) -> str:
        """Send code to Groq for review."""
        try:
            code_content = file_path.read_text()
            file_name = file_path.name
            
            prompt = f"""You are an expert code reviewer. Please review the following {file_path.suffix} file and provide:

1. **Architecture Assessment**: Overall design patterns and structure
2. **Code Quality**: Readability, maintainability, and adherence to best practices
3. **Potential Bugs**: Any issues that might cause runtime errors or unexpected behavior
4. **Performance Concerns**: Inefficiencies or optimization opportunities
5. **Security Issues**: Any potential vulnerabilities
6. **Suggestions**: Specific improvements with code examples where applicable

File: {file_name}
```{file_path.suffix[1:] if file_path.suffix else 'text'}
{code_content}
```

Provide a detailed, constructive review focused on actionable improvements."""

            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a senior software engineer conducting a thorough code review."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4096
                }
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Error during code review: {e}"


def load_api_key() -> Optional[str]:
    """Load Groq API key from ~/.env file."""
    env_path = Path.home() / ".env"
    
    if not env_path.exists():
        print("Error: ~/.env file not found")
        return None
        
    load_dotenv(env_path)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("Error: GROQ_API_KEY not found in ~/.env")
        return None
        
    return api_key


def main():
    parser = argparse.ArgumentParser(
        description="Get AI-powered code review using Groq API"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the file to review"
    )
    parser.add_argument(
        "--model",
        help="Specific model to use (otherwise auto-selects best available)"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models and exit"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Save review to file instead of printing"
    )
    
    args = parser.parse_args()
    
    # Load API key
    api_key = load_api_key()
    if not api_key:
        sys.exit(1)
        
    reviewer = GroqCodeReviewer(api_key)
    
    # Get available models
    print("🔍 Fetching available Groq models...")
    models = reviewer.get_available_models()
    
    if not models:
        print("Error: No models available")
        sys.exit(1)
    
    # List models if requested
    if args.list_models:
        print("\n📋 Available Groq Models:")
        for model in models:
            print(f"  - {model['id']}")
        sys.exit(0)
    
    # Check file exists
    if not args.file.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    # Select model
    if args.model:
        selected_model = args.model
        available_ids = {m["id"] for m in models}
        if selected_model not in available_ids:
            print(f"Error: Model '{selected_model}' not available")
            print("Use --list-models to see available options")
            sys.exit(1)
    else:
        selected_model = reviewer.select_best_model(models)
        if not selected_model:
            print("Error: Could not select a suitable model")
            sys.exit(1)
    
    print(f"✨ Using model: {selected_model}")
    print(f"📄 Reviewing: {args.file}")
    print("⏳ Generating review...\n")
    
    # Get review
    review = reviewer.review_code(args.file, selected_model)
    
    # Output results
    if args.output:
        args.output.write_text(review)
        print(f"✅ Review saved to: {args.output}")
    else:
        print("=" * 80)
        print(f"Code Review for: {args.file.name}")
        print(f"Model: {selected_model}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(review)


if __name__ == "__main__":
    main()