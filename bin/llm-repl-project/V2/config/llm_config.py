"""LLM Configuration for different providers and models."""

from dataclasses import dataclass
from plugins.llm_interface import LLMProvider


@dataclass
class LLMConfiguration:
    """Configuration for different LLM providers and models for different cognitive processes."""
    intent_detection_provider: LLMProvider = LLMProvider.OLLAMA
    intent_detection_model: str = "llama3.2:1b"
    
    main_query_provider: LLMProvider = LLMProvider.OLLAMA  
    main_query_model: str = "llama3.2:3b"
    
    @property
    def intent_detection_display_name(self) -> str:
        """Display name for intent detection model."""
        if self.intent_detection_provider == LLMProvider.OLLAMA:
            return f"ollama/{self.intent_detection_model}"
        elif self.intent_detection_provider == LLMProvider.GROQ:
            return f"groq/{self.intent_detection_model}"
        else:
            return f"{self.intent_detection_provider.value}/{self.intent_detection_model}"
    
    @property
    def main_query_display_name(self) -> str:
        """Display name for main query model."""
        if self.main_query_provider == LLMProvider.OLLAMA:
            return f"ollama/{self.main_query_model}"
        elif self.main_query_provider == LLMProvider.GROQ:
            return f"groq/{self.main_query_model}"
        else:
            return f"{self.main_query_provider.value}/{self.main_query_model}"


# Predefined configurations
CONFIGURATIONS = {
    "debug": LLMConfiguration(
        intent_detection_provider=LLMProvider.OLLAMA,
        intent_detection_model="tinyllama",  # Use actual tinyllama model
        main_query_provider=LLMProvider.OLLAMA,
        main_query_model="tinyllama"  # Use actual tinyllama model
    ),
    "mixed": LLMConfiguration(
        intent_detection_provider=LLMProvider.OLLAMA,
        intent_detection_model="tinyllama",  # Use actual tinyllama model
        main_query_provider=LLMProvider.GROQ,
        main_query_model="llama3-8b-8192"  # Use Groq for main query
    ),
    "fast": LLMConfiguration(
        intent_detection_provider=LLMProvider.GROQ,
        intent_detection_model="llama3-8b-8192",
        main_query_provider=LLMProvider.GROQ,
        main_query_model="llama3-8b-8192"
    ),
    "test": LLMConfiguration(
        intent_detection_provider=LLMProvider.GROQ,
        intent_detection_model="llama3-8b-8192",  # Use Groq for testing (faster, no local setup needed)
        main_query_provider=LLMProvider.GROQ,
        main_query_model="llama3-8b-8192"  # Use Groq for both to avoid Ollama dependency
    )
}