"""Groq LLM provider implementation."""

import aiohttp
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .base import BaseLLMProvider, LLMProvider, LLMResponse


class GroqProvider(BaseLLMProvider):
    """Groq provider implementation."""
    
    def _get_provider(self) -> LLMProvider:
        return LLMProvider.GROQ
    
    def _get_api_key(self) -> str:
        """Get API key from environment or .env file."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            # Try loading from ~/.env file
            env_file = Path.home() / ".env"
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith("GROQ_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                            break
        
        if not api_key:
            raise Exception("GROQ_API_KEY not found in environment variables or ~/.env file")
        
        return api_key
    
    async def make_request(self, prompt: str, options: Dict[str, Any] = None) -> LLMResponse:
        """Execute Groq request."""
        api_key = self._get_api_key()
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        options = options or {}
        
        # Convert prompt to chat format
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "temperature": options.get("temperature", 0.7),
            "max_tokens": options.get("max_tokens", 1024)
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        raise Exception(f"HTTP {resp.status}: {error_text}")
                    
                    data = await resp.json()
                    duration = time.time() - start_time
                    
                    # Extract response content
                    content = ""
                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0]["message"]["content"]
                    
                    # Extract token usage
                    usage = data.get("usage", {})
                    input_tokens = usage.get("prompt_tokens", 0)
                    output_tokens = usage.get("completion_tokens", 0)
                    
                    return self._create_response(
                        content=content,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        duration=duration,
                        metadata=data
                    )
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to connect to Groq API: {str(e)}")
        except Exception as e:
            if "GROQ_API_KEY" in str(e):
                raise
            raise Exception(f"Groq request failed: {str(e)}")