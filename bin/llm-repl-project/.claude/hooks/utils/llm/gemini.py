#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "google-generativeai",
#     "python-dotenv",
# ]
# ///

import os
import sys
from dotenv import load_dotenv


def prompt_llm(prompt_text):
    """
    Base Gemini LLM prompting method using fastest model.

    Args:
        prompt_text (str): The prompt to send to the model

    Returns:
        str: The model's response text, or None if error
    """
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')  # Fastest Gemini model
        
        response = model.generate_content(
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.7
            )
        )
        
        return response.text.strip()
        
    except Exception:
        return None


def main():
    """Main entry point for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--completion', action='store_true', 
                       help='Generate a session completion message')
    parser.add_argument('prompt', nargs='?', 
                       help='Custom prompt text')
    
    args = parser.parse_args()
    
    if args.completion:
        # Generate session completion message
        prompt = """Generate a brief, professional completion message for a coding session. 
        Keep it under 20 words. Focus on what was accomplished. 
        Examples: "Successfully implemented user authentication", "Completed API refactoring", "Fixed critical bugs in payment system"."""
        
        result = prompt_llm(prompt)
        if result:
            print(result)
        else:
            print("Session completed successfully.")
    
    elif args.prompt:
        result = prompt_llm(args.prompt)
        if result:
            print(result)
        else:
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()