"""Ollama LLM provider implementation."""

import aiohttp
import time
from typing import Any, Dict, Optional

from .base import BaseLLMProvider, LLMProvider, LLMResponse


class OllamaProvider(BaseLLMProvider):
    """Ollama provider implementation."""
    
    def _get_provider(self) -> LLMProvider:
        return LLMProvider.OLLAMA
    
    async def make_request(self, prompt: str, options: Dict[str, Any] = None) -> LLMResponse:
        """Execute Ollama request."""
        url = f"{self.base_url or 'http://localhost:11434'}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options or {}
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status != 200:
                        raise Exception(f"HTTP {resp.status}: {await resp.text()}")
                    
                    data = await resp.json()
                    duration = time.time() - start_time
                    
                    return self._create_response(
                        content=data.get("response", ""),
                        input_tokens=data.get("prompt_eval_count", 0),
                        output_tokens=data.get("eval_count", 0),
                        duration=duration,
                        metadata=data
                    )
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama request failed: {str(e)}")