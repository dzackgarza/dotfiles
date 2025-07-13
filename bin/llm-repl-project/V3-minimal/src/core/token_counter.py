"""
Real-Time Token Counting System

Implements Task 12.2: Accurate token counting for context management,
API limit enforcement, and performance optimization.
"""

import re
import json
import hashlib
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import lru_cache


@dataclass
class TokenCount:
    """Token count result with metadata."""
    text: str
    token_count: int
    method: str
    cached: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TokenCounterBase(ABC):
    """Abstract base class for token counting implementations."""
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        pass
    
    @abstractmethod
    def get_method_name(self) -> str:
        """Get the name of this counting method."""
        pass


class SimpleTokenCounter(TokenCounterBase):
    """
    Simple token counter using heuristic approximation.
    
    Fast fallback when advanced tokenizers aren't available.
    Based on OpenAI's rough approximation of 1 token ≈ 4 characters.
    """
    
    def count_tokens(self, text: str) -> int:
        """Approximate token count using character-based heuristics."""
        if not text.strip():
            return 0
        
        # Basic preprocessing
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # Character-based approximation with adjustments
        char_count = len(cleaned_text)
        
        # Adjust for different text patterns
        # Technical text tends to have fewer tokens per character
        technical_adjustment = 1.0
        if self._is_technical_text(cleaned_text):
            technical_adjustment = 0.85
        
        # Conversational text tends to have more tokens per character  
        conversational_adjustment = 1.0
        if self._is_conversational_text(cleaned_text):
            conversational_adjustment = 1.15
        
        # Apply OpenAI's ~4 chars per token rule with adjustments
        estimated_tokens = (char_count / 4.0) * technical_adjustment * conversational_adjustment
        
        return max(1, int(round(estimated_tokens)))
    
    def get_method_name(self) -> str:
        return "simple_heuristic"
    
    def _is_technical_text(self, text: str) -> bool:
        """Detect if text contains technical content."""
        technical_indicators = [
            r'\b\w+\(\)',  # Function calls
            r'\b[A-Z_]+\b',  # Constants
            r'[{}[\]();]',  # Code brackets
            r'\b\d+\.\d+\b',  # Version numbers
            r'\bdef\b|\bclass\b|\bimport\b|\bfrom\b',  # Python keywords
        ]
        
        technical_matches = sum(
            len(re.findall(pattern, text)) 
            for pattern in technical_indicators
        )
        
        return technical_matches > len(text) / 100  # >1% technical content
    
    def _is_conversational_text(self, text: str) -> bool:
        """Detect if text is conversational."""
        conversational_indicators = [
            r'\?',  # Questions
            r'!',  # Exclamations  
            r'\bi\b|\byou\b|\bwe\b|\bthey\b',  # Personal pronouns
            r'\bwell\b|\bokay\b|\bhmm\b|\boh\b',  # Interjections
            r'\bthanks\b|\bplease\b|\bsorry\b',  # Polite words
        ]
        
        conversational_matches = sum(
            len(re.findall(pattern, text, re.IGNORECASE))
            for pattern in conversational_indicators
        )
        
        return conversational_matches > len(text.split()) / 20  # >5% conversational


class TikTokenCounter(TokenCounterBase):
    """
    Accurate token counter using tiktoken library.
    
    Provides exact token counts for OpenAI models.
    Falls back to SimpleTokenCounter if tiktoken unavailable.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.encoding = None
        self.fallback_counter = SimpleTokenCounter()
        
        try:
            import tiktoken
            self.encoding = tiktoken.encoding_for_model(model_name)
        except ImportError:
            print("Warning: tiktoken not available, falling back to simple counter")
        except Exception as e:
            print(f"Warning: tiktoken error ({e}), falling back to simple counter")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken or fallback to simple counter."""
        if self.encoding is None:
            return self.fallback_counter.count_tokens(text)
        
        try:
            return len(self.encoding.encode(text))
        except Exception:
            # Fallback if encoding fails
            return self.fallback_counter.count_tokens(text)
    
    def get_method_name(self) -> str:
        if self.encoding is None:
            return f"tiktoken_fallback_{self.fallback_counter.get_method_name()}"
        return f"tiktoken_{self.model_name}"


class CachedTokenCounter:
    """
    Token counter with intelligent caching for performance.
    
    Caches token counts with content hashing to avoid recalculation
    of identical text blocks. Includes performance optimizations:
    - LRU cache with configurable size
    - Batch processing support
    - Memory-efficient hashing
    - Fast cache hit detection
    """
    
    def __init__(self, 
                 base_counter: TokenCounterBase = None,
                 cache_size: int = 2000):  # Increased default cache size
        self.base_counter = base_counter or TikTokenCounter()
        self.cache_size = cache_size
        self._cache: Dict[str, TokenCount] = {}
        self._access_order: List[str] = []
        self._cache_hits = 0
        self._total_requests = 0
    
    def count_tokens(self, text: str, include_metadata: bool = True) -> Union[int, TokenCount]:
        """
        Count tokens with caching.
        
        Args:
            text: Text to count tokens for
            include_metadata: Return TokenCount object with metadata
        
        Returns:
            Token count (int) or TokenCount object with metadata
        """
        self._total_requests += 1
        
        # Early return for empty text
        if not text.strip():
            empty_result = TokenCount(
                text=text,
                token_count=0,
                method=self.base_counter.get_method_name(),
                cached=False,
                metadata={"text_length": 0, "word_count": 0, "chars_per_token": 0}
            )
            return empty_result if include_metadata else 0
        
        # Generate cache key from text hash
        cache_key = self._generate_cache_key(text)
        
        # Check cache first
        if cache_key in self._cache:
            self._cache_hits += 1
            cached_result = self._cache[cache_key]
            self._update_access_order(cache_key)
            
            if include_metadata:
                # Return copy with cached flag set
                return TokenCount(
                    text=text,
                    token_count=cached_result.token_count,
                    method=cached_result.method,
                    cached=True,
                    metadata=cached_result.metadata.copy()
                )
            return cached_result.token_count
        
        # Calculate new token count
        token_count = self.base_counter.count_tokens(text)
        
        # Create result object
        result = TokenCount(
            text=text,
            token_count=token_count,
            method=self.base_counter.get_method_name(),
            cached=False,
            metadata={
                "text_length": len(text),
                "word_count": len(text.split()),
                "chars_per_token": len(text) / token_count if token_count > 0 else 0
            }
        )
        
        # Cache the result
        self._cache_result(cache_key, result)
        
        return result if include_metadata else token_count
    
    def count_tokens_batch(self, texts: List[str]) -> List[TokenCount]:
        """Count tokens for multiple texts efficiently with batch optimizations."""
        results = []
        
        # Pre-generate cache keys for all texts to minimize repeated hashing
        cache_keys = [self._generate_cache_key(text) for text in texts]
        
        # Separate cached vs uncached texts for batch processing
        cached_results = {}
        uncached_texts = []
        uncached_indices = []
        
        for i, (text, cache_key) in enumerate(zip(texts, cache_keys)):
            if cache_key in self._cache:
                self._cache_hits += 1
                cached_results[i] = self._cache[cache_key]
                self._update_access_order(cache_key)
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # Process uncached texts
        uncached_results = {}
        for idx, text in zip(uncached_indices, uncached_texts):
            self._total_requests += 1
            token_count = self.base_counter.count_tokens(text)
            
            result = TokenCount(
                text=text,
                token_count=token_count,
                method=self.base_counter.get_method_name(),
                cached=False,
                metadata={
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "chars_per_token": len(text) / token_count if token_count > 0 else 0
                }
            )
            
            # Cache the result
            self._cache_result(cache_keys[idx], result)
            uncached_results[idx] = result
        
        # Combine results in original order
        for i, text in enumerate(texts):
            if i in cached_results:
                cached_result = cached_results[i]
                result = TokenCount(
                    text=text,
                    token_count=cached_result.token_count,
                    method=cached_result.method,
                    cached=True,
                    metadata=cached_result.metadata.copy()
                )
            else:
                result = uncached_results[i]
            
            results.append(result)
        
        return results
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        return {
            "cache_size": len(self._cache),
            "max_cache_size": self.cache_size,
            "total_requests": self._total_requests,
            "cache_hits": self._cache_hits,
            "hit_rate": self._cache_hits / self._total_requests if self._total_requests > 0 else 0.0,
            "memory_efficiency": len(self._cache) / self.cache_size if self.cache_size > 0 else 0.0,
            "counter_method": self.base_counter.get_method_name()
        }
    
    def clear_cache(self):
        """Clear the token count cache."""
        self._cache.clear()
        self._access_order.clear()
    
    def _generate_cache_key(self, text: str) -> str:
        """Generate cache key from text content."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _cache_result(self, cache_key: str, result: TokenCount):
        """Cache a token count result with LRU eviction."""
        # Evict oldest if cache is full
        if len(self._cache) >= self.cache_size and cache_key not in self._cache:
            oldest_key = self._access_order.pop(0)
            del self._cache[oldest_key]
        
        # Add new result
        self._cache[cache_key] = result
        self._update_access_order(cache_key)
    
    def _update_access_order(self, cache_key: str):
        """Update access order for LRU tracking."""
        if cache_key in self._access_order:
            self._access_order.remove(cache_key)
        self._access_order.append(cache_key)


class ConversationTokenManager:
    """
    High-level token management for conversations.
    
    Tracks token usage across conversation turns and provides
    intelligent context window management.
    """
    
    def __init__(self, 
                 token_counter: CachedTokenCounter = None,
                 context_window_size: int = 4096,
                 system_prompt_tokens: int = 100,
                 response_buffer_tokens: int = 500):
        """
        Initialize conversation token manager.
        
        Args:
            token_counter: Token counting implementation
            context_window_size: Maximum tokens for model context
            system_prompt_tokens: Tokens reserved for system prompt
            response_buffer_tokens: Tokens reserved for response generation
        """
        self.token_counter = token_counter or CachedTokenCounter()
        self.context_window_size = context_window_size
        self.system_prompt_tokens = system_prompt_tokens
        self.response_buffer_tokens = response_buffer_tokens
        
        # Available tokens for conversation context
        self.available_context_tokens = (
            context_window_size - 
            system_prompt_tokens - 
            response_buffer_tokens
        )
    
    def count_conversation_tokens(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Count tokens for a complete conversation.
        
        Args:
            messages: List of conversation messages with 'role' and 'content'
        
        Returns:
            Dictionary with token counts and analysis
        """
        total_tokens = 0
        message_tokens = []
        
        for message in messages:
            content = message.get('content', '')
            count_result = self.token_counter.count_tokens(content, include_metadata=True)
            
            message_info = {
                'role': message.get('role', 'unknown'),
                'content_preview': content[:50] + '...' if len(content) > 50 else content,
                'token_count': count_result.token_count,
                'cached': count_result.cached
            }
            
            message_tokens.append(message_info)
            total_tokens += count_result.token_count
        
        return {
            'total_tokens': total_tokens,
            'message_count': len(messages),
            'average_tokens_per_message': total_tokens / len(messages) if messages else 0,
            'messages': message_tokens,
            'fits_in_context': total_tokens <= self.available_context_tokens,
            'available_tokens': self.available_context_tokens,
            'overflow_tokens': max(0, total_tokens - self.available_context_tokens)
        }
    
    def optimize_context_for_query(self, 
                                  messages: List[Dict[str, str]],
                                  new_query: str) -> Dict[str, Any]:
        """
        Optimize conversation context for a new query.
        
        Uses token counting + context scoring to select optimal messages.
        """
        # Count tokens for new query (use simple count)
        query_tokens = self.token_counter.count_tokens(new_query, include_metadata=False)
        
        # Adjust available tokens for the new query
        adjusted_available = self.available_context_tokens - query_tokens
        
        # Convert messages to conversation turns for scoring
        from .context_scoring import ConversationTurn, advanced_context_scorer
        from datetime import datetime, timezone
        
        turns = []
        for i, msg in enumerate(messages):
            # Use message index as crude timestamp
            timestamp = datetime.now(timezone.utc).replace(microsecond=i * 1000)
            turn = ConversationTurn(
                id=str(i),
                content=msg.get('content', ''),
                role=msg.get('role', 'unknown'),
                timestamp=timestamp,
                tokens=self.token_counter.count_tokens(msg.get('content', ''), include_metadata=False)
            )
            turns.append(turn)
        
        # Get optimal context selection
        selected_turns = advanced_context_scorer.get_optimal_context(
            turns,
            new_query,
            max_tokens=adjusted_available
        )
        
        # Convert back to message format
        selected_messages = []
        total_selected_tokens = 0
        
        for turn in selected_turns:
            original_msg = messages[int(turn.id)]
            selected_messages.append(original_msg)
            total_selected_tokens += turn.tokens
        
        return {
            'original_message_count': len(messages),
            'selected_message_count': len(selected_messages),
            'selected_messages': selected_messages,
            'original_tokens': sum(self.token_counter.count_tokens(msg.get('content', ''), include_metadata=False) for msg in messages),
            'selected_tokens': total_selected_tokens,
            'query_tokens': query_tokens,
            'total_context_tokens': total_selected_tokens + query_tokens,
            'token_reduction': len(messages) - len(selected_messages),
            'optimization_successful': total_selected_tokens + query_tokens <= self.available_context_tokens
        }


# Global token counter instances
simple_counter = SimpleTokenCounter()
tiktoken_counter = TikTokenCounter()
cached_counter = CachedTokenCounter(tiktoken_counter)
conversation_manager = ConversationTokenManager(cached_counter)