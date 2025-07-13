"""
Tests for Token Counting System

Validates Task 12.2 implementation with real token counting scenarios.
"""

import pytest
from datetime import datetime, timezone
from src.core.token_counter import (
    SimpleTokenCounter,
    TikTokenCounter,
    CachedTokenCounter,
    ConversationTokenManager,
    TokenCount
)


class TestSimpleTokenCounter:
    """Test basic heuristic token counting."""
    
    def setup_method(self):
        self.counter = SimpleTokenCounter()
    
    def test_empty_text(self):
        """Empty text should return 0 tokens."""
        assert self.counter.count_tokens("") == 0
        assert self.counter.count_tokens("   ") == 0
    
    def test_simple_text(self):
        """Basic text should have reasonable token count."""
        text = "Hello world, how are you today?"
        tokens = self.counter.count_tokens(text)
        # Rough expectation: ~6-8 tokens for this simple text
        assert 5 <= tokens <= 10
    
    def test_technical_text_adjustment(self):
        """Technical text should have lower chars-per-token ratio."""
        technical = "def calculate_tokens(text: str) -> int: return len(encoding.encode(text))"
        conversational = "Hey there! How are you doing today? I hope everything is going well for you!"
        
        tech_tokens = self.counter.count_tokens(technical)
        conv_tokens = self.counter.count_tokens(conversational)
        
        # Technical text should be more token-dense
        tech_ratio = len(technical) / tech_tokens
        conv_ratio = len(conversational) / conv_tokens
        assert tech_ratio < conv_ratio
    
    def test_method_name(self):
        """Should return correct method name."""
        assert self.counter.get_method_name() == "simple_heuristic"


class TestTikTokenCounter:
    """Test tiktoken-based counting with fallback."""
    
    def setup_method(self):
        self.counter = TikTokenCounter()
    
    def test_basic_counting(self):
        """Should count tokens for basic text."""
        text = "Hello, world!"
        tokens = self.counter.count_tokens(text)
        assert isinstance(tokens, int)
        assert tokens > 0
    
    def test_empty_text(self):
        """Empty text should return 0."""
        assert self.counter.count_tokens("") == 0
    
    def test_method_name(self):
        """Should return appropriate method name."""
        method = self.counter.get_method_name()
        assert "tiktoken" in method or "fallback" in method
    
    def test_consistency(self):
        """Same text should always return same count."""
        text = "This is a test message for consistency checking."
        count1 = self.counter.count_tokens(text)
        count2 = self.counter.count_tokens(text)
        assert count1 == count2


class TestCachedTokenCounter:
    """Test cached token counting with performance optimization."""
    
    def setup_method(self):
        self.counter = CachedTokenCounter(cache_size=10)
    
    def test_caching_behavior(self):
        """Should cache results and mark them as cached."""
        text = "This text will be cached for performance testing."
        
        # First call - not cached
        result1 = self.counter.count_tokens(text, include_metadata=True)
        assert isinstance(result1, TokenCount)
        assert not result1.cached
        assert result1.token_count > 0
        
        # Second call - should be cached
        result2 = self.counter.count_tokens(text, include_metadata=True)
        assert result2.cached
        assert result2.token_count == result1.token_count
    
    def test_cache_stats(self):
        """Should track cache performance statistics."""
        texts = [
            "First unique text",
            "Second unique text", 
            "First unique text",  # Repeat
            "Third unique text"
        ]
        
        for text in texts:
            self.counter.count_tokens(text)
        
        stats = self.counter.get_cache_stats()
        assert stats["cache_size"] == 3  # 3 unique texts
        assert stats["total_requests"] >= 4
        assert stats["hit_rate"] > 0  # Should have cache hits
    
    def test_batch_counting(self):
        """Should efficiently count multiple texts."""
        texts = [
            "First batch text",
            "Second batch text",
            "Third batch text"
        ]
        
        results = self.counter.count_tokens_batch(texts)
        assert len(results) == 3
        assert all(isinstance(r, TokenCount) for r in results)
        assert all(r.token_count > 0 for r in results)
    
    def test_cache_eviction(self):
        """Should evict old entries when cache is full."""
        # Fill cache beyond capacity
        for i in range(15):  # Cache size is 10
            self.counter.count_tokens(f"Text number {i}")
        
        stats = self.counter.get_cache_stats()
        assert stats["cache_size"] <= 10  # Should not exceed limit
    
    def test_metadata_inclusion(self):
        """Should include useful metadata in results."""
        text = "Test text for metadata validation"
        result = self.counter.count_tokens(text, include_metadata=True)
        
        assert "text_length" in result.metadata
        assert "word_count" in result.metadata
        assert "chars_per_token" in result.metadata
        assert result.metadata["text_length"] == len(text)
        assert result.metadata["word_count"] == len(text.split())


class TestConversationTokenManager:
    """Test high-level conversation token management."""
    
    def setup_method(self):
        self.manager = ConversationTokenManager(
            context_window_size=1000,
            system_prompt_tokens=50,
            response_buffer_tokens=100
        )
        
        # Available context tokens = 1000 - 50 - 100 = 850
        assert self.manager.available_context_tokens == 850
    
    def test_conversation_token_counting(self):
        """Should count tokens for complete conversations."""
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "Can you help me with Python programming?"},
            {"role": "assistant", "content": "Absolutely! I'd be happy to help with Python."}
        ]
        
        result = self.manager.count_conversation_tokens(messages)
        
        assert "total_tokens" in result
        assert "message_count" in result
        assert "fits_in_context" in result
        assert result["message_count"] == 4
        assert result["total_tokens"] > 0
        assert len(result["messages"]) == 4
    
    def test_context_optimization(self):
        """Should optimize context for new queries."""
        # Create a long conversation that exceeds context window
        messages = []
        for i in range(20):
            messages.append({
                "role": "user", 
                "content": f"This is user message number {i} with some content to make it longer."
            })
            messages.append({
                "role": "assistant",
                "content": f"This is assistant response number {i} with detailed information and explanations."
            })
        
        new_query = "Tell me about the most recent topic we discussed."
        
        result = self.manager.optimize_context_for_query(messages, new_query)
        
        assert "original_message_count" in result
        assert "selected_message_count" in result
        assert "optimization_successful" in result
        assert result["selected_message_count"] <= result["original_message_count"]
        assert result["total_context_tokens"] <= self.manager.available_context_tokens
    
    def test_empty_conversation(self):
        """Should handle empty conversations gracefully."""
        result = self.manager.count_conversation_tokens([])
        
        assert result["total_tokens"] == 0
        assert result["message_count"] == 0
        assert result["average_tokens_per_message"] == 0
        assert result["fits_in_context"] is True
    
    def test_single_long_message(self):
        """Should handle messages that exceed context window."""
        very_long_content = "This is a very long message. " * 200  # Create long text
        
        messages = [{"role": "user", "content": very_long_content}]
        result = self.manager.count_conversation_tokens(messages)
        
        assert result["total_tokens"] > 0
        # Should detect if it fits in context
        if result["total_tokens"] > self.manager.available_context_tokens:
            assert not result["fits_in_context"]
            assert result["overflow_tokens"] > 0


class TestRealWorldScenarios:
    """Test token counting with realistic use cases."""
    
    def setup_method(self):
        self.manager = ConversationTokenManager()
    
    def test_programming_conversation(self):
        """Test token counting for programming discussions."""
        messages = [
            {
                "role": "user",
                "content": "How do I implement a binary search algorithm in Python?"
            },
            {
                "role": "assistant", 
                "content": """Here's a binary search implementation:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

This algorithm has O(log n) time complexity."""
            },
            {
                "role": "user",
                "content": "Can you explain the time complexity in more detail?"
            }
        ]
        
        result = self.manager.count_conversation_tokens(messages)
        
        # Code should be counted accurately
        assert result["total_tokens"] > 50  # Should be substantial due to code
        assert all(msg["token_count"] > 0 for msg in result["messages"])
    
    def test_multilingual_content(self):
        """Test token counting with different languages."""
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "user", "content": "Bonjour, comment allez-vous?"},  # French
            {"role": "user", "content": "Hola, ¿cómo estás?"},  # Spanish
            {"role": "user", "content": "こんにちは、元気ですか？"},  # Japanese
        ]
        
        result = self.manager.count_conversation_tokens(messages)
        
        # All messages should be counted
        assert result["message_count"] == 4
        assert all(msg["token_count"] > 0 for msg in result["messages"])
    
    def test_markdown_and_formatting(self):
        """Test token counting with formatted text."""
        formatted_content = """
# Heading 1

This is **bold text** and *italic text*.

## Code Example

```python
def hello_world():
    print("Hello, World!")
```

- List item 1
- List item 2
- List item 3

[Link text](https://example.com)
        """.strip()
        
        messages = [{"role": "assistant", "content": formatted_content}]
        result = self.manager.count_conversation_tokens(messages)
        
        # Markdown formatting should be counted appropriately
        assert result["total_tokens"] > 20
        assert result["messages"][0]["token_count"] > 0


class TestTokenCounterIntegration:
    """Test integration between different token counter components."""
    
    def test_counter_consistency(self):
        """Different counters should give similar results for same text."""
        text = "This is a test message for comparing different token counters."
        
        simple_count = SimpleTokenCounter().count_tokens(text)
        tiktoken_count = TikTokenCounter().count_tokens(text)
        
        # Should be in the same ballpark (within 50% of each other)
        ratio = max(simple_count, tiktoken_count) / min(simple_count, tiktoken_count)
        assert ratio <= 2.0  # Allow up to 2x difference
    
    def test_cached_vs_direct(self):
        """Cached counter should match direct counter results."""
        text = "Test message for cache consistency validation."
        
        direct_counter = TikTokenCounter()
        cached_counter = CachedTokenCounter(direct_counter)
        
        direct_count = direct_counter.count_tokens(text)
        cached_result = cached_counter.count_tokens(text, include_metadata=True)
        
        assert cached_result.token_count == direct_count
        assert not cached_result.cached  # First call shouldn't be cached
        
        # Second call should be cached but same result
        cached_result2 = cached_counter.count_tokens(text, include_metadata=True)
        assert cached_result2.token_count == direct_count
        assert cached_result2.cached


if __name__ == "__main__":
    pytest.main([__file__, "-v"])