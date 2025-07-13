"""
Context Formatting Logic

Implements Task 12.3: Sophisticated formatting strategies for presenting 
conversation context to AI models in an optimal, structured way.
"""

import re
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any, Union, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

from .context_scoring import ConversationTurn
from .summarization import (
    ContextSummarizationManager, 
    ConversationSummary, 
    SummaryConfig,
    get_summarization_manager
)


class FormatStyle(Enum):
    """Different formatting styles for various use cases."""
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    STRUCTURED = "structured"
    MINIMAL = "minimal"
    CHAT_ML = "chatml"  # ChatML format for OpenAI models


@dataclass
class FormatSettings:
    """Configuration for context formatting."""
    style: FormatStyle = FormatStyle.CONVERSATIONAL
    include_timestamps: bool = True
    include_token_counts: bool = False
    include_relevance_scores: bool = False
    max_content_length: Optional[int] = None
    preserve_code_blocks: bool = True
    add_turn_numbers: bool = False
    role_prefixes: bool = True
    
    # Summarization settings
    enable_summarization: bool = True
    max_context_tokens: int = 4000
    summarization_config: Optional[SummaryConfig] = None


@dataclass
class FormattedContext:
    """Result of context formatting operation."""
    formatted_text: str
    total_tokens: int
    turn_count: int
    metadata: Dict[str, Any]
    truncated_turns: List[str] = None
    summaries_used: List[ConversationSummary] = None
    
    def __post_init__(self):
        if self.truncated_turns is None:
            self.truncated_turns = []
        if self.summaries_used is None:
            self.summaries_used = []


class ContextFormatter(ABC):
    """Abstract base for different context formatting strategies."""
    
    @abstractmethod
    def format_context(self, 
                      turns: List[ConversationTurn],
                      settings: FormatSettings = None) -> FormattedContext:
        """Format conversation turns into structured context."""
        pass
    
    @abstractmethod
    def format_single_turn(self, 
                          turn: ConversationTurn,
                          settings: FormatSettings = None) -> str:
        """Format a single conversation turn."""
        pass


class ConversationalFormatter(ContextFormatter):
    """
    Formats context in a natural, conversational style.
    
    Optimized for general-purpose conversation with clear role separation
    and natural flow that feels like reading a conversation transcript.
    """
    
    def format_context(self, 
                      turns: List[ConversationTurn],
                      settings: FormatSettings = None) -> FormattedContext:
        """Format turns in conversational style."""
        settings = settings or FormatSettings()
        
        formatted_parts = []
        total_tokens = 0
        truncated_turns = []
        
        # Add context header
        if len(turns) > 1:
            formatted_parts.append(self._create_context_header(turns, settings))
        
        # Format each turn
        for i, turn in enumerate(turns):
            formatted_turn = self.format_single_turn(turn, settings)
            
            # Check if content needs truncation
            if settings.max_content_length and len(formatted_turn) > settings.max_content_length:
                truncated_turn = self._truncate_content(formatted_turn, settings.max_content_length)
                formatted_parts.append(truncated_turn)
                truncated_turns.append(turn.id)
            else:
                formatted_parts.append(formatted_turn)
            
            total_tokens += turn.tokens
        
        # Join with appropriate separators
        separator = "\n\n" if settings.style == FormatStyle.CONVERSATIONAL else "\n"
        formatted_text = separator.join(formatted_parts)
        
        return FormattedContext(
            formatted_text=formatted_text,
            total_tokens=total_tokens,
            turn_count=len(turns),
            truncated_turns=truncated_turns,
            metadata={
                "style": settings.style.value,
                "settings": settings.__dict__
            }
        )
    
    def format_single_turn(self, 
                          turn: ConversationTurn,
                          settings: FormatSettings = None) -> str:
        """Format a single turn in conversational style."""
        settings = settings or FormatSettings()
        
        parts = []
        
        # Role prefix
        if settings.role_prefixes:
            role_prefix = self._get_role_prefix(turn.role)
            parts.append(role_prefix)
        
        # Timestamp
        if settings.include_timestamps:
            timestamp = self._format_timestamp(turn.timestamp)
            parts.append(f"[{timestamp}]")
        
        # Content with proper formatting
        content = self._format_content(turn.content, settings)
        
        # Combine parts
        prefix = " ".join(parts)
        if prefix:
            return f"{prefix}\n{content}"
        return content
    
    def _create_context_header(self, turns: List[ConversationTurn], settings: FormatSettings) -> str:
        """Create informative header for context window."""
        start_time = min(turn.timestamp for turn in turns)
        end_time = max(turn.timestamp for turn in turns)
        
        duration = end_time - start_time
        hours = duration.total_seconds() / 3600
        
        if hours < 1:
            time_span = f"{int(duration.total_seconds() / 60)} minutes"
        elif hours < 24:
            time_span = f"{hours:.1f} hours"
        else:
            time_span = f"{hours/24:.1f} days"
        
        return f"--- Previous conversation ({len(turns)} turns over {time_span}) ---"
    
    def _get_role_prefix(self, role: str) -> str:
        """Get appropriate prefix for conversation role."""
        role_prefixes = {
            "user": "User:",
            "assistant": "Assistant:",
            "system": "System:",
            "function": "Function:",
            "tool": "Tool:"
        }
        return role_prefixes.get(role.lower(), f"{role.title()}:")
    
    def _format_timestamp(self, timestamp: datetime) -> str:
        """Format timestamp for display."""
        now = datetime.now(timezone.utc)
        diff = now - timestamp
        
        if diff.total_seconds() < 3600:  # Less than 1 hour
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes}m ago"
        elif diff.total_seconds() < 86400:  # Less than 1 day
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            days = int(diff.total_seconds() / 86400)
            return f"{days}d ago"
    
    def _format_content(self, content: str, settings: FormatSettings) -> str:
        """Format content with proper structure preservation."""
        if not settings.preserve_code_blocks:
            return content
        
        # Preserve code blocks and formatting
        formatted = content
        
        # Ensure code blocks are properly separated
        formatted = re.sub(r'```(\w+)?\n', r'```\1\n', formatted)
        
        # Clean up excessive whitespace while preserving intentional formatting
        lines = formatted.split('\n')
        cleaned_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                cleaned_lines.append(line)
            elif in_code_block:
                cleaned_lines.append(line)  # Preserve exact formatting in code
            else:
                cleaned_lines.append(line.rstrip())  # Remove trailing whitespace
        
        return '\n'.join(cleaned_lines)
    
    def _truncate_content(self, content: str, max_length: int) -> str:
        """Intelligently truncate content while preserving structure."""
        if len(content) <= max_length:
            return content
        
        # Try to truncate at sentence boundaries
        sentences = re.split(r'[.!?]+\s+', content)
        truncated = ""
        
        for sentence in sentences:
            if len(truncated + sentence) + 20 > max_length:  # Leave room for ellipsis
                break
            truncated += sentence + ". "
        
        if not truncated:  # Fallback to character truncation
            truncated = content[:max_length-10]
        
        return truncated.rstrip() + "... [truncated]"


class TechnicalFormatter(ContextFormatter):
    """
    Formats context for technical/programming discussions.
    
    Emphasizes code structure, technical details, and precise formatting
    optimized for programming assistance and technical documentation.
    """
    
    def format_context(self, 
                      turns: List[ConversationTurn],
                      settings: FormatSettings = None) -> FormattedContext:
        """Format turns in technical style."""
        settings = settings or FormatSettings(style=FormatStyle.TECHNICAL)
        
        formatted_parts = []
        total_tokens = 0
        
        # Technical header with metadata
        header = self._create_technical_header(turns, settings)
        formatted_parts.append(header)
        
        # Format each turn with technical focus
        for i, turn in enumerate(turns):
            turn_header = f"## Turn {i+1} [{turn.role.upper()}]"
            if settings.include_timestamps:
                timestamp = turn.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
                turn_header += f" - {timestamp}"
            if settings.include_token_counts:
                turn_header += f" ({turn.tokens} tokens)"
            
            formatted_parts.append(turn_header)
            formatted_parts.append(self.format_single_turn(turn, settings))
            total_tokens += turn.tokens
        
        formatted_text = "\n\n".join(formatted_parts)
        
        return FormattedContext(
            formatted_text=formatted_text,
            total_tokens=total_tokens,
            turn_count=len(turns),
            metadata={
                "style": "technical",
                "structure": "markdown",
                "code_blocks_preserved": True
            }
        )
    
    def format_single_turn(self, 
                          turn: ConversationTurn,
                          settings: FormatSettings = None) -> str:
        """Format single turn with technical emphasis."""
        content = turn.content
        
        # Enhance code block formatting
        content = self._enhance_code_blocks(content)
        
        # Add technical metadata if requested
        if settings and settings.include_relevance_scores and hasattr(turn, 'relevance_score'):
            content += f"\n\n*[Relevance: {turn.relevance_score:.2f}]*"
        
        return content
    
    def _create_technical_header(self, turns: List[ConversationTurn], settings: FormatSettings) -> str:
        """Create technical documentation style header."""
        total_tokens = sum(turn.tokens for turn in turns)
        start_time = min(turn.timestamp for turn in turns)
        end_time = max(turn.timestamp for turn in turns)
        
        return f"""# Conversation Context
**Turns:** {len(turns)} | **Total Tokens:** {total_tokens} | **Timespan:** {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}

---"""
    
    def _enhance_code_blocks(self, content: str) -> str:
        """Enhance code block formatting for technical clarity."""
        # Add line numbers to code blocks
        def add_line_numbers(match):
            language = match.group(1) or ""
            code = match.group(2)
            lines = code.split('\n')
            
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                if line.strip():  # Only number non-empty lines
                    numbered_lines.append(f"{i:3d} | {line}")
                else:
                    numbered_lines.append(line)
            
            return f"```{language}\n" + '\n'.join(numbered_lines) + "\n```"
        
        # Apply line numbering to code blocks
        enhanced = re.sub(r'```(\w+)?\n(.*?)\n```', add_line_numbers, content, flags=re.DOTALL)
        
        return enhanced


class StructuredFormatter(ContextFormatter):
    """
    Formats context with explicit structure and metadata.
    
    Uses JSON-like or XML-like structured format for precise parsing
    and maximum information preservation for model understanding.
    """
    
    def format_context(self, 
                      turns: List[ConversationTurn],
                      settings: FormatSettings = None) -> FormattedContext:
        """Format turns in structured format."""
        settings = settings or FormatSettings(style=FormatStyle.STRUCTURED)
        
        structured_turns = []
        total_tokens = 0
        
        for turn in turns:
            structured_turn = {
                "id": turn.id,
                "role": turn.role,
                "timestamp": turn.timestamp.isoformat(),
                "content": turn.content,
                "tokens": turn.tokens
            }
            
            if hasattr(turn, 'metadata') and turn.metadata:
                structured_turn["metadata"] = turn.metadata
            
            structured_turns.append(structured_turn)
            total_tokens += turn.tokens
        
        # Format as readable structured text
        formatted_parts = ["<conversation_context>"]
        
        for turn_data in structured_turns:
            turn_xml = f"""<turn id="{turn_data['id']}" role="{turn_data['role']}" tokens="{turn_data['tokens']}">
<timestamp>{turn_data['timestamp']}</timestamp>
<content>
{turn_data['content']}
</content>
</turn>"""
            formatted_parts.append(turn_xml)
        
        formatted_parts.append("</conversation_context>")
        
        return FormattedContext(
            formatted_text="\n\n".join(formatted_parts),
            total_tokens=total_tokens,
            turn_count=len(turns),
            metadata={
                "style": "structured",
                "format": "xml",
                "machine_readable": True
            }
        )
    
    def format_single_turn(self, 
                          turn: ConversationTurn,
                          settings: FormatSettings = None) -> str:
        """Format single turn in structured format."""
        return f"""<turn role="{turn.role}" id="{turn.id}">
<content>{turn.content}</content>
</turn>"""


class ChatMLFormatter(ContextFormatter):
    """
    Formats context in ChatML format for OpenAI models.
    
    Uses the official ChatML format specification for optimal
    compatibility with OpenAI's chat completion models.
    """
    
    def format_context(self, 
                      turns: List[ConversationTurn],
                      settings: FormatSettings = None) -> FormattedContext:
        """Format turns in ChatML format."""
        formatted_parts = []
        total_tokens = 0
        
        for turn in turns:
            formatted_turn = self.format_single_turn(turn, settings)
            formatted_parts.append(formatted_turn)
            total_tokens += turn.tokens
        
        return FormattedContext(
            formatted_text="\n".join(formatted_parts),
            total_tokens=total_tokens,
            turn_count=len(turns),
            metadata={
                "style": "chatml",
                "openai_compatible": True
            }
        )
    
    def format_single_turn(self, 
                          turn: ConversationTurn,
                          settings: FormatSettings = None) -> str:
        """Format single turn in ChatML format."""
        return f"<|im_start|>{turn.role}\n{turn.content}<|im_end|>"


class ContextFormattingManager:
    """
    High-level manager for context formatting operations.
    
    Coordinates between different formatting strategies and provides
    intelligent format selection based on content analysis.
    """
    
    def __init__(self):
        self.formatters = {
            FormatStyle.CONVERSATIONAL: ConversationalFormatter(),
            FormatStyle.TECHNICAL: TechnicalFormatter(),
            FormatStyle.STRUCTURED: StructuredFormatter(),
            FormatStyle.CHAT_ML: ChatMLFormatter()
        }
        self._summarization_manager = None
    
    async def format_context(self,
                      turns: List[ConversationTurn],
                      style: Union[FormatStyle, str] = FormatStyle.CONVERSATIONAL,
                      settings: FormatSettings = None) -> FormattedContext:
        """
        Format conversation context using specified style with optional summarization.
        
        Args:
            turns: Conversation turns to format
            style: Formatting style to use
            settings: Additional formatting settings
        
        Returns:
            FormattedContext with structured output
        """
        if isinstance(style, str):
            style = FormatStyle(style)
        
        if settings is None:
            settings = FormatSettings(style=style)
        else:
            settings.style = style
        
        # Apply summarization if enabled
        processed_turns = turns
        summaries_used = []
        
        if settings.enable_summarization and len(turns) > 5:
            processed_turns, summaries_used = await self._apply_summarization(turns, settings)
        
        formatter = self.formatters.get(style)
        if not formatter:
            raise ValueError(f"Unsupported formatting style: {style}")
        
        # Format the processed turns
        result = formatter.format_context(processed_turns, settings)
        
        # Add summary information to result
        if summaries_used:
            result.summaries_used = summaries_used
            result.metadata['summarization_applied'] = True
            result.metadata['summaries_count'] = len(summaries_used)
            
            # Prepend summary information to formatted text
            summary_text = self._format_summaries(summaries_used, style)
            if summary_text:
                result.formatted_text = summary_text + "\n\n" + result.formatted_text
        
        return result
    
    def suggest_format_style(self, turns: List[ConversationTurn]) -> FormatStyle:
        """
        Suggest optimal formatting style based on content analysis.
        
        Analyzes conversation content to recommend the most appropriate
        formatting style for the given context.
        """
        if not turns:
            return FormatStyle.CONVERSATIONAL
        
        # Analyze content characteristics
        total_content = " ".join(turn.content for turn in turns)
        
        # Count technical indicators
        code_blocks = len(re.findall(r'```', total_content))
        code_keywords = len(re.findall(r'\b(function|class|import|from|def|var|let|const)\b', total_content, re.IGNORECASE))
        file_paths = len(re.findall(r'[./]?\w+/\w+', total_content))
        
        # Count structured data indicators
        json_indicators = len(re.findall(r'[{}\[\]]', total_content))
        xml_indicators = len(re.findall(r'<[^>]+>', total_content))
        
        technical_score = code_blocks * 3 + code_keywords + file_paths
        structured_score = json_indicators + xml_indicators * 2
        
        # Recommend based on analysis
        if technical_score > 5:
            return FormatStyle.TECHNICAL
        elif structured_score > 10:
            return FormatStyle.STRUCTURED
        else:
            return FormatStyle.CONVERSATIONAL
    
    async def optimize_for_model(self, 
                          turns: List[ConversationTurn],
                          model_name: str = "gpt-3.5-turbo") -> FormattedContext:
        """
        Optimize formatting for specific AI model.
        
        Uses model-specific formatting strategies for optimal performance.
        """
        # Model-specific optimization rules
        if "gpt" in model_name.lower():
            # OpenAI models work well with ChatML or conversational
            style = FormatStyle.CHAT_ML if len(turns) > 5 else FormatStyle.CONVERSATIONAL
        elif "claude" in model_name.lower():
            # Claude models prefer structured conversation
            style = FormatStyle.CONVERSATIONAL
        elif "code" in model_name.lower():
            # Code-focused models prefer technical formatting
            style = FormatStyle.TECHNICAL
        else:
            # Default to content-based suggestion
            style = self.suggest_format_style(turns)
        
        settings = FormatSettings(
            style=style,
            include_timestamps=True,
            preserve_code_blocks=True,
            role_prefixes=True
        )
        
        return await self.format_context(turns, style, settings)
    
    async def _apply_summarization(self, 
                                 turns: List[ConversationTurn], 
                                 settings: FormatSettings) -> Tuple[List[ConversationTurn], List[ConversationSummary]]:
        """Apply summarization to conversation turns if needed"""
        if self._summarization_manager is None:
            summary_config = settings.summarization_config or SummaryConfig(
                max_context_tokens=settings.max_context_tokens
            )
            self._summarization_manager = get_summarization_manager(config=summary_config)
        
        # Process turns for summarization
        remaining_turns, summaries = await self._summarization_manager.process_conversation_for_summarization(
            turns, force_summarize=False
        )
        
        return remaining_turns, summaries
    
    def _format_summaries(self, summaries: List[ConversationSummary], style: FormatStyle) -> str:
        """Format summaries for inclusion in context"""
        if not summaries:
            return ""
        
        if style == FormatStyle.CHAT_ML:
            summary_parts = []
            for summary in summaries:
                summary_parts.append(f"<|summary|>{summary.content}<|/summary|>")
            return "\n".join(summary_parts)
        
        elif style == FormatStyle.TECHNICAL:
            summary_parts = []
            for summary in summaries:
                summary_parts.append(f"// SUMMARY: {summary.summary_id}")
                summary_parts.append(f"// Compressed {summary.metadata.turns_summarized} turns "
                                   f"({summary.metadata.compression_ratio:.1f}x compression)")
                summary_parts.append(summary.content)
                summary_parts.append("")
            return "\n".join(summary_parts)
        
        elif style == FormatStyle.STRUCTURED:
            summary_parts = []
            summary_parts.append("=== CONVERSATION SUMMARIES ===")
            for summary in summaries:
                summary_parts.append(f"Summary ID: {summary.summary_id}")
                summary_parts.append(f"Time Span: {summary.metadata.time_span_hours:.1f} hours")
                summary_parts.append(f"Turns: {summary.metadata.turns_summarized}")
                summary_parts.append(f"Content: {summary.content}")
                summary_parts.append("---")
            summary_parts.append("=== END SUMMARIES ===")
            return "\n".join(summary_parts)
        
        else:  # CONVERSATIONAL
            summary_parts = []
            summary_parts.append("## Previous Conversation Summary")
            for i, summary in enumerate(summaries, 1):
                if len(summaries) > 1:
                    summary_parts.append(f"### Summary {i} ({summary.metadata.time_span_hours:.1f}h ago)")
                summary_parts.append(summary.content)
                if summary.key_topics:
                    summary_parts.append(f"*Key topics: {', '.join(summary.key_topics[:3])}*")
                summary_parts.append("")
            return "\n".join(summary_parts)


# Global formatting manager instance
context_formatting_manager = ContextFormattingManager()