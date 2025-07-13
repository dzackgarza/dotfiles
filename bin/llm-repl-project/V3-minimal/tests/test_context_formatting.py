"""
Tests for Context Formatting System

Validates Task 12.3 implementation with various formatting scenarios.
"""

import pytest
from datetime import datetime, timezone, timedelta
from src.core.context_formatting import (
    FormatStyle,
    FormatSettings,
    FormattedContext,
    ConversationalFormatter,
    TechnicalFormatter,
    StructuredFormatter,
    ChatMLFormatter,
    ContextFormattingManager
)
from src.core.context_scoring import ConversationTurn


class TestFormatSettings:
    """Test format settings configuration."""
    
    def test_default_settings(self):
        """Test default format settings."""
        settings = FormatSettings()
        assert settings.style == FormatStyle.CONVERSATIONAL
        assert settings.include_timestamps is True
        assert settings.include_token_counts is False
        assert settings.preserve_code_blocks is True
        assert settings.role_prefixes is True
    
    def test_custom_settings(self):
        """Test custom format settings."""
        settings = FormatSettings(
            style=FormatStyle.TECHNICAL,
            include_timestamps=False,
            include_token_counts=True,
            max_content_length=500
        )
        
        assert settings.style == FormatStyle.TECHNICAL
        assert settings.include_timestamps is False
        assert settings.include_token_counts is True
        assert settings.max_content_length == 500


class TestConversationalFormatter:
    """Test conversational formatting style."""
    
    def setup_method(self):
        self.formatter = ConversationalFormatter()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str, minutes_ago: int = 0) -> ConversationTurn:
        """Helper to create test conversation turns."""
        timestamp = self.current_time - timedelta(minutes=minutes_ago)
        return ConversationTurn(
            id=f"turn_{role}_{minutes_ago}",
            content=content,
            role=role,
            timestamp=timestamp,
            tokens=50
        )
    
    def test_single_turn_formatting(self):
        """Test formatting of a single conversation turn."""
        turn = self.create_test_turn("Hello, how are you?", "user", 30)
        
        formatted = self.formatter.format_single_turn(turn)
        
        assert "User:" in formatted
        assert "30m ago" in formatted
        assert "Hello, how are you?" in formatted
    
    def test_role_prefixes(self):
        """Test proper role prefix formatting."""
        user_turn = self.create_test_turn("Question", "user")
        assistant_turn = self.create_test_turn("Answer", "assistant")
        
        user_formatted = self.formatter.format_single_turn(user_turn)
        assistant_formatted = self.formatter.format_single_turn(assistant_turn)
        
        assert "User:" in user_formatted
        assert "Assistant:" in assistant_formatted
    
    def test_timestamp_formatting(self):
        """Test various timestamp format outputs."""
        recent_turn = self.create_test_turn("Recent", "user", 15)  # 15 minutes ago
        old_turn = self.create_test_turn("Old", "user", 120)      # 2 hours ago
        
        recent_formatted = self.formatter.format_single_turn(recent_turn)
        old_formatted = self.formatter.format_single_turn(old_turn)
        
        assert "15m ago" in recent_formatted
        assert "2h ago" in old_formatted
    
    def test_context_formatting(self):
        """Test formatting of multiple conversation turns."""
        turns = [
            self.create_test_turn("First question", "user", 60),
            self.create_test_turn("First answer", "assistant", 58),
            self.create_test_turn("Follow-up question", "user", 30),
        ]
        
        result = self.formatter.format_context(turns)
        
        assert isinstance(result, FormattedContext)
        assert result.turn_count == 3
        assert result.total_tokens == 150  # 3 turns * 50 tokens each
        assert "Previous conversation" in result.formatted_text
        assert "User:" in result.formatted_text
        assert "Assistant:" in result.formatted_text
    
    def test_code_block_preservation(self):
        """Test that code blocks are preserved correctly."""
        code_content = """Here's some Python code:

```python
def hello_world():
    print("Hello, World!")
    return True
```

This function prints a greeting."""
        
        turn = self.create_test_turn(code_content, "assistant")
        result = self.formatter.format_single_turn(turn)
        
        assert "```python" in result
        assert "def hello_world():" in result
        assert "```" in result
    
    def test_content_truncation(self):
        """Test content truncation when max length is set."""
        long_content = "This is a very long message. " * 50  # 1500+ characters
        turn = self.create_test_turn(long_content, "user")
        
        settings = FormatSettings(max_content_length=200)
        result = self.formatter.format_context([turn], settings)
        
        assert "[truncated]" in result.formatted_text
        assert len(turn.id) in result.truncated_turns
    
    def test_settings_without_timestamps(self):
        """Test formatting with timestamps disabled."""
        turn = self.create_test_turn("Test message", "user", 30)
        settings = FormatSettings(include_timestamps=False)
        
        result = self.formatter.format_single_turn(turn, settings)
        
        assert "30m ago" not in result
        assert "User:" in result
        assert "Test message" in result


class TestTechnicalFormatter:
    """Test technical formatting style."""
    
    def setup_method(self):
        self.formatter = TechnicalFormatter()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str, minutes_ago: int = 0) -> ConversationTurn:
        """Helper to create test conversation turns."""
        timestamp = self.current_time - timedelta(minutes=minutes_ago)
        return ConversationTurn(
            id=f"turn_{role}_{minutes_ago}",
            content=content,
            role=role,
            timestamp=timestamp,
            tokens=75
        )
    
    def test_technical_header(self):
        """Test technical documentation style header."""
        turns = [
            self.create_test_turn("Code question", "user", 30),
            self.create_test_turn("Code answer", "assistant", 28),
        ]
        
        result = self.formatter.format_context(turns)
        
        assert "# Conversation Context" in result.formatted_text
        assert "**Turns:** 2" in result.formatted_text
        assert "**Total Tokens:** 150" in result.formatted_text
    
    def test_turn_headers(self):
        """Test technical turn headers with metadata."""
        turn = self.create_test_turn("Technical content", "user", 15)
        settings = FormatSettings(
            include_timestamps=True,
            include_token_counts=True
        )
        
        result = self.formatter.format_context([turn], settings)
        
        assert "## Turn 1 [USER]" in result.formatted_text
        assert "UTC" in result.formatted_text
        assert "(75 tokens)" in result.formatted_text
    
    def test_code_block_enhancement(self):
        """Test enhancement of code blocks with line numbers."""
        code_content = """Here's a function:

```python
def calculate_sum(a, b):
    result = a + b
    return result
```

The function adds two numbers."""
        
        turn = self.create_test_turn(code_content, "assistant")
        result = self.formatter.format_single_turn(turn)
        
        # Check for line numbering
        assert "  1 | def calculate_sum(a, b):" in result
        assert "  2 |     result = a + b" in result
        assert "  3 |     return result" in result


class TestStructuredFormatter:
    """Test structured XML-like formatting."""
    
    def setup_method(self):
        self.formatter = StructuredFormatter()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str, turn_id: str = None) -> ConversationTurn:
        """Helper to create test conversation turns."""
        return ConversationTurn(
            id=turn_id or f"turn_{role}",
            content=content,
            role=role,
            timestamp=self.current_time,
            tokens=40
        )
    
    def test_xml_structure(self):
        """Test XML-like structured output."""
        turns = [
            self.create_test_turn("Question", "user", "turn_1"),
            self.create_test_turn("Answer", "assistant", "turn_2"),
        ]
        
        result = self.formatter.format_context(turns)
        
        assert "<conversation_context>" in result.formatted_text
        assert "</conversation_context>" in result.formatted_text
        assert '<turn id="turn_1" role="user"' in result.formatted_text
        assert '<turn id="turn_2" role="assistant"' in result.formatted_text
        assert "<timestamp>" in result.formatted_text
        assert "<content>" in result.formatted_text
    
    def test_metadata_preservation(self):
        """Test that metadata is preserved in structured format."""
        result = self.formatter.format_context([
            self.create_test_turn("Test content", "user")
        ])
        
        assert result.metadata["style"] == "structured"
        assert result.metadata["format"] == "xml"
        assert result.metadata["machine_readable"] is True
    
    def test_single_turn_xml(self):
        """Test single turn XML formatting."""
        turn = self.create_test_turn("Test message", "user", "test_id")
        result = self.formatter.format_single_turn(turn)
        
        assert '<turn role="user" id="test_id">' in result
        assert '<content>Test message</content>' in result
        assert '</turn>' in result


class TestChatMLFormatter:
    """Test ChatML formatting for OpenAI models."""
    
    def setup_method(self):
        self.formatter = ChatMLFormatter()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str) -> ConversationTurn:
        """Helper to create test conversation turns."""
        return ConversationTurn(
            id=f"turn_{role}",
            content=content,
            role=role,
            timestamp=self.current_time,
            tokens=30
        )
    
    def test_chatml_format(self):
        """Test ChatML format compliance."""
        turns = [
            self.create_test_turn("Hello", "user"),
            self.create_test_turn("Hi there!", "assistant"),
        ]
        
        result = self.formatter.format_context(turns)
        
        assert "<|im_start|>user\nHello<|im_end|>" in result.formatted_text
        assert "<|im_start|>assistant\nHi there!<|im_end|>" in result.formatted_text
        assert result.metadata["openai_compatible"] is True
    
    def test_single_turn_chatml(self):
        """Test single turn ChatML formatting."""
        turn = self.create_test_turn("Test message", "user")
        result = self.formatter.format_single_turn(turn)
        
        assert result == "<|im_start|>user\nTest message<|im_end|>"


class TestContextFormattingManager:
    """Test high-level formatting manager."""
    
    def setup_method(self):
        self.manager = ContextFormattingManager()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str) -> ConversationTurn:
        """Helper to create test conversation turns."""
        return ConversationTurn(
            id=f"turn_{role}",
            content=content,
            role=role,
            timestamp=self.current_time,
            tokens=50
        )
    
    def test_style_selection(self):
        """Test different formatting styles."""
        turns = [self.create_test_turn("Hello", "user")]
        
        # Test each style
        conv_result = self.manager.format_context(turns, FormatStyle.CONVERSATIONAL)
        tech_result = self.manager.format_context(turns, FormatStyle.TECHNICAL)
        struct_result = self.manager.format_context(turns, FormatStyle.STRUCTURED)
        chatml_result = self.manager.format_context(turns, FormatStyle.CHAT_ML)
        
        assert "User:" in conv_result.formatted_text
        assert "# Conversation Context" in tech_result.formatted_text
        assert "<conversation_context>" in struct_result.formatted_text
        assert "<|im_start|>" in chatml_result.formatted_text
    
    def test_format_style_suggestion(self):
        """Test automatic format style suggestion."""
        # Technical content
        code_turns = [
            self.create_test_turn("Here's some code:\n```python\ndef hello():\n    pass\n```", "assistant")
        ]
        
        # Regular conversation
        chat_turns = [
            self.create_test_turn("How are you today?", "user")
        ]
        
        # Structured data
        structured_turns = [
            self.create_test_turn("Here's the JSON: {\"key\": \"value\", \"array\": [1, 2, 3]}", "assistant")
        ]
        
        assert self.manager.suggest_format_style(code_turns) == FormatStyle.TECHNICAL
        assert self.manager.suggest_format_style(chat_turns) == FormatStyle.CONVERSATIONAL
        assert self.manager.suggest_format_style(structured_turns) == FormatStyle.STRUCTURED
    
    def test_model_optimization(self):
        """Test model-specific formatting optimization."""
        turns = [self.create_test_turn("Test message", "user")]
        
        # Test different model optimizations
        gpt_result = self.manager.optimize_for_model(turns, "gpt-3.5-turbo")
        claude_result = self.manager.optimize_for_model(turns, "claude-3-sonnet")
        code_result = self.manager.optimize_for_model(turns, "code-davinci-002")
        
        # Should return different formatting styles
        assert isinstance(gpt_result, FormattedContext)
        assert isinstance(claude_result, FormattedContext)
        assert isinstance(code_result, FormattedContext)
    
    def test_string_style_conversion(self):
        """Test string to FormatStyle conversion."""
        turns = [self.create_test_turn("Test", "user")]
        
        result = self.manager.format_context(turns, "technical")
        assert "# Conversation Context" in result.formatted_text
    
    def test_invalid_style_handling(self):
        """Test handling of invalid formatting styles."""
        turns = [self.create_test_turn("Test", "user")]
        
        with pytest.raises(ValueError, match="Unsupported formatting style"):
            self.manager.format_context(turns, "invalid_style")


class TestRealWorldScenarios:
    """Test formatting with realistic conversation scenarios."""
    
    def setup_method(self):
        self.manager = ContextFormattingManager()
        self.current_time = datetime.now(timezone.utc)
    
    def test_programming_help_conversation(self):
        """Test formatting of programming help conversation."""
        turns = [
            ConversationTurn(
                "1", "How do I sort a list in Python?", "user",
                self.current_time - timedelta(minutes=5), 25
            ),
            ConversationTurn(
                "2", """You can use the `sort()` method:

```python
my_list = [3, 1, 4, 1, 5]
my_list.sort()
print(my_list)  # [1, 1, 3, 4, 5]
```

Or use `sorted()` for a new list:

```python
new_list = sorted(my_list)
```""", "assistant",
                self.current_time - timedelta(minutes=4), 120
            ),
            ConversationTurn(
                "3", "What about sorting in reverse order?", "user",
                self.current_time - timedelta(minutes=2), 30
            )
        ]
        
        # Test technical formatting
        result = self.manager.format_context(turns, FormatStyle.TECHNICAL)
        
        assert "```python" in result.formatted_text
        assert "sort()" in result.formatted_text
        assert "## Turn" in result.formatted_text
        assert result.turn_count == 3
        assert result.total_tokens == 175
    
    def test_mixed_content_conversation(self):
        """Test formatting with mixed content types."""
        turns = [
            ConversationTurn(
                "1", "What's the weather like?", "user",
                self.current_time - timedelta(hours=1), 20
            ),
            ConversationTurn(
                "2", "I can't check real-time weather, but here's how to get weather data via API:", "assistant",
                self.current_time - timedelta(hours=1), 60
            ),
            ConversationTurn(
                "3", """```json
{
  "weather": {
    "temperature": 22,
    "condition": "sunny",
    "humidity": 45
  }
}
```""", "assistant",
                self.current_time - timedelta(minutes=58), 80
            )
        ]
        
        # Should suggest technical format due to code content
        suggested_style = self.manager.suggest_format_style(turns)
        assert suggested_style == FormatStyle.TECHNICAL
        
        result = self.manager.format_context(turns, suggested_style)
        assert "```json" in result.formatted_text
        assert "weather" in result.formatted_text
    
    def test_long_conversation_formatting(self):
        """Test formatting of long conversations."""
        # Create 10 turns over several hours
        turns = []
        for i in range(10):
            role = "user" if i % 2 == 0 else "assistant"
            content = f"Message {i+1} in this long conversation"
            timestamp = self.current_time - timedelta(hours=i/2)
            
            turns.append(ConversationTurn(
                str(i+1), content, role, timestamp, 25
            ))
        
        result = self.manager.format_context(turns, FormatStyle.CONVERSATIONAL)
        
        assert result.turn_count == 10
        assert result.total_tokens == 250
        assert "Previous conversation (10 turns" in result.formatted_text
        
        # Should handle timestamps correctly
        assert "5h ago" in result.formatted_text  # Oldest turn
        assert "0m ago" in result.formatted_text or "1m ago" in result.formatted_text  # Newest turn
    
    def test_truncation_with_settings(self):
        """Test content truncation with various settings."""
        long_content = """This is a very long technical explanation about how neural networks work. 
Neural networks are computational models inspired by biological neural networks. 
They consist of layers of interconnected nodes (neurons) that process information 
through weighted connections. The learning process involves adjusting these weights 
based on training data to minimize prediction errors. This is achieved through 
backpropagation and gradient descent algorithms."""
        
        turn = ConversationTurn(
            "1", long_content, "assistant", self.current_time, 200
        )
        
        settings = FormatSettings(
            style=FormatStyle.CONVERSATIONAL,
            max_content_length=150,
            include_timestamps=True
        )
        
        result = self.manager.format_context([turn], FormatStyle.CONVERSATIONAL, settings)
        
        assert "[truncated]" in result.formatted_text
        assert "1" in result.truncated_turns
        assert len(result.formatted_text) < len(long_content) + 100  # Should be significantly shorter


if __name__ == "__main__":
    pytest.main([__file__, "-v"])