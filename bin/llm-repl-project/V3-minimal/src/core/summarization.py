#!/usr/bin/env python3
"""
Context Summarization System

Implements automated summarization of older conversation turns to reduce
context window size while preserving key information.
"""

import asyncio
import logging
import threading
import queue
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Union
import json
import hashlib
from pathlib import Path
import concurrent.futures

from .context_scoring import ConversationTurn, ContextScore, AdvancedContextScorer
from .token_counter import ConversationTokenManager, TokenCount


class SummarizationTrigger(Enum):
    """Triggers for when summarization should occur"""
    TOKEN_THRESHOLD = auto()    # When token count exceeds limit
    TIME_THRESHOLD = auto()     # When content is older than threshold
    RELEVANCE_THRESHOLD = auto() # When relevance score drops below threshold
    MANUAL = auto()             # Manually requested


class SummaryType(Enum):
    """Types of summaries that can be generated"""
    EXTRACTIVE = auto()         # Extract key sentences/phrases
    ABSTRACTIVE = auto()        # Generate new summary text
    HIERARCHICAL = auto()       # Multi-level summary structure
    SEMANTIC = auto()           # Preserve semantic relationships


@dataclass
class SummaryConfig:
    """Configuration for summarization behavior"""
    # Token thresholds
    max_context_tokens: int = 4000
    summary_target_tokens: int = 500
    min_tokens_to_summarize: int = 100
    
    # Time thresholds
    max_age_hours: float = 24.0
    stale_threshold_hours: float = 6.0
    
    # Relevance thresholds
    min_relevance_score: float = 0.3
    preserve_high_relevance: float = 0.8
    
    # Summary behavior
    preserve_recent_turns: int = 5
    min_turns_to_summarize: int = 3
    max_summary_ratio: float = 0.25  # Summary should be max 25% of original
    
    # Quality controls
    min_summary_quality: float = 0.7
    enable_quality_verification: bool = True
    
    # Cache settings
    cache_summaries: bool = True
    cache_duration_hours: float = 12.0


@dataclass
class SummaryMetadata:
    """Metadata about a generated summary"""
    summary_id: str
    source_turn_ids: List[str]
    created_at: datetime
    summary_type: SummaryType
    trigger_reason: SummarizationTrigger
    
    # Quality metrics
    compression_ratio: float  # Original tokens / summary tokens
    relevance_preserved: float  # How much relevance was retained
    information_density: float  # Information per token in summary
    
    # Source statistics
    original_token_count: int
    summary_token_count: int
    turns_summarized: int
    time_span_hours: float


@dataclass
class ConversationSummary:
    """A summary of conversation turns"""
    summary_id: str
    content: str
    metadata: SummaryMetadata
    source_turns: List[ConversationTurn] = field(default_factory=list)
    
    # Contextual information
    key_topics: List[str] = field(default_factory=list)
    important_entities: List[str] = field(default_factory=list)
    semantic_vectors: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'summary_id': self.summary_id,
            'content': self.content,
            'metadata': {
                'summary_id': self.metadata.summary_id,
                'source_turn_ids': self.metadata.source_turn_ids,
                'created_at': self.metadata.created_at.isoformat(),
                'summary_type': self.metadata.summary_type.name,
                'trigger_reason': self.metadata.trigger_reason.name,
                'compression_ratio': self.metadata.compression_ratio,
                'relevance_preserved': self.metadata.relevance_preserved,
                'information_density': self.metadata.information_density,
                'original_token_count': self.metadata.original_token_count,
                'summary_token_count': self.metadata.summary_token_count,
                'turns_summarized': self.metadata.turns_summarized,
                'time_span_hours': self.metadata.time_span_hours
            },
            'key_topics': self.key_topics,
            'important_entities': self.important_entities,
            'semantic_vectors': self.semantic_vectors
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationSummary':
        """Create from dictionary"""
        metadata_dict = data['metadata']
        metadata = SummaryMetadata(
            summary_id=metadata_dict['summary_id'],
            source_turn_ids=metadata_dict['source_turn_ids'],
            created_at=datetime.fromisoformat(metadata_dict['created_at']),
            summary_type=SummaryType[metadata_dict['summary_type']],
            trigger_reason=SummarizationTrigger[metadata_dict['trigger_reason']],
            compression_ratio=metadata_dict['compression_ratio'],
            relevance_preserved=metadata_dict['relevance_preserved'],
            information_density=metadata_dict['information_density'],
            original_token_count=metadata_dict['original_token_count'],
            summary_token_count=metadata_dict['summary_token_count'],
            turns_summarized=metadata_dict['turns_summarized'],
            time_span_hours=metadata_dict['time_span_hours']
        )
        
        return cls(
            summary_id=data['summary_id'],
            content=data['content'],
            metadata=metadata,
            key_topics=data.get('key_topics', []),
            important_entities=data.get('important_entities', []),
            semantic_vectors=data.get('semantic_vectors')
        )


class SummarizationService:
    """Service for generating summaries of conversation content with background processing"""
    
    def __init__(self, config: SummaryConfig = None):
        self.config = config or SummaryConfig()
        self.logger = logging.getLogger(__name__)
        
        # Initialize dependencies
        self.token_manager = ConversationTokenManager()
        self.context_scorer = AdvancedContextScorer()
        
        # Summary cache
        self._summary_cache: Dict[str, ConversationSummary] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        
        # Background processing
        self._background_queue = queue.Queue()
        self._background_thread = None
        self._background_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._shutdown_event = threading.Event()
        self._processing_lock = threading.Lock()
        
        # Start background summarization thread (temporarily disabled)
        # self._start_background_processing()
    
    def should_summarize(self, 
                        turns: List[ConversationTurn],
                        current_token_count: int = None) -> Tuple[bool, SummarizationTrigger]:
        """
        Determine if conversation turns should be summarized.
        
        Returns:
            Tuple of (should_summarize, trigger_reason)
        """
        if len(turns) < self.config.min_turns_to_summarize:
            return False, None
        
        # Check token threshold
        if current_token_count is None:
            token_result = self.token_manager.count_conversation_tokens(
                [{'role': turn.role, 'content': turn.content} for turn in turns]
            )
            # Extract total tokens from the result dictionary
            current_token_count = token_result.get('total_tokens', 0)
        
        if current_token_count > self.config.max_context_tokens:
            return True, SummarizationTrigger.TOKEN_THRESHOLD
        
        # Check time threshold
        if turns:
            oldest_turn = min(turns, key=lambda t: t.timestamp)
            # Ensure timezone consistency
            now = datetime.now(timezone.utc) if oldest_turn.timestamp.tzinfo else datetime.now()
            age_hours = (now - oldest_turn.timestamp).total_seconds() / 3600
            
            if age_hours > self.config.max_age_hours:
                return True, SummarizationTrigger.TIME_THRESHOLD
        
        # Check relevance threshold (for older turns)
        if len(turns) > self.config.preserve_recent_turns:
            older_turns = turns[:-self.config.preserve_recent_turns]
            avg_relevance = self._calculate_average_relevance(older_turns)
            
            if avg_relevance < self.config.min_relevance_score:
                return True, SummarizationTrigger.RELEVANCE_THRESHOLD
        
        return False, None
    
    def _calculate_average_relevance(self, turns: List[ConversationTurn]) -> float:
        """Calculate average relevance score for turns"""
        if not turns:
            return 1.0
        
        scores = []
        for turn in turns:
            # Get relevance score from context scorer (using simplified approach)
            # In a real implementation, this would use the full context scoring system
            scores.append(0.5)  # Default relevance score for testing
        
        return sum(scores) / len(scores) if scores else 0.0
    
    async def generate_summary(self, 
                             turns: List[ConversationTurn],
                             summary_type: SummaryType = SummaryType.EXTRACTIVE,
                             trigger: SummarizationTrigger = SummarizationTrigger.MANUAL) -> ConversationSummary:
        """
        Generate a summary of conversation turns.
        
        Args:
            turns: Conversation turns to summarize
            summary_type: Type of summary to generate
            trigger: What triggered this summarization
        
        Returns:
            Generated conversation summary
        """
        if not turns:
            raise ValueError("Cannot summarize empty conversation")
        
        # Generate unique summary ID
        turn_ids = [turn.id for turn in turns]
        content_hash = hashlib.md5(
            "".join(turn.content for turn in turns).encode()
        ).hexdigest()[:8]
        summary_id = f"summary_{content_hash}_{len(turns)}turns"
        
        # Check cache first
        if self.config.cache_summaries and summary_id in self._summary_cache:
            cached_summary = self._summary_cache[summary_id]
            cache_time = self._cache_timestamps[summary_id]
            
            # Check if cache is still valid
            cache_age = datetime.now() - cache_time
            if cache_age.total_seconds() / 3600 < self.config.cache_duration_hours:
                self.logger.debug(f"Using cached summary: {summary_id}")
                return cached_summary
        
        # Calculate original token count
        token_result = self.token_manager.count_conversation_tokens(
            [{'role': turn.role, 'content': turn.content} for turn in turns]
        )
        original_tokens = token_result.get('total_tokens', 0)
        
        # Generate summary based on type
        if summary_type == SummaryType.EXTRACTIVE:
            summary_content = await self._generate_extractive_summary(turns)
        elif summary_type == SummaryType.ABSTRACTIVE:
            summary_content = await self._generate_abstractive_summary(turns)
        elif summary_type == SummaryType.HIERARCHICAL:
            summary_content = await self._generate_hierarchical_summary(turns)
        else:
            # Default to extractive
            summary_content = await self._generate_extractive_summary(turns)
        
        # Count summary tokens
        summary_tokens = self.token_manager.token_counter.count_tokens(summary_content, include_metadata=False)
        
        # Calculate metrics
        compression_ratio = original_tokens / max(summary_tokens, 1)
        time_span = (max(turns, key=lambda t: t.timestamp).timestamp - 
                    min(turns, key=lambda t: t.timestamp).timestamp).total_seconds() / 3600
        
        # Estimate relevance preservation (simplified)
        relevance_preserved = min(1.0, self.config.summary_target_tokens / max(summary_tokens, 1))
        information_density = summary_tokens / max(len(summary_content.split()), 1)
        
        # Create metadata
        metadata = SummaryMetadata(
            summary_id=summary_id,
            source_turn_ids=turn_ids,
            created_at=datetime.now(),
            summary_type=summary_type,
            trigger_reason=trigger,
            compression_ratio=compression_ratio,
            relevance_preserved=relevance_preserved,
            information_density=information_density,
            original_token_count=original_tokens,
            summary_token_count=summary_tokens,
            turns_summarized=len(turns),
            time_span_hours=time_span
        )
        
        # Extract topics and entities
        key_topics = self._extract_topics(turns)
        important_entities = self._extract_entities(turns)
        
        # Create summary object
        summary = ConversationSummary(
            summary_id=summary_id,
            content=summary_content,
            metadata=metadata,
            source_turns=turns,
            key_topics=key_topics,
            important_entities=important_entities
        )
        
        # Cache the summary
        if self.config.cache_summaries:
            self._summary_cache[summary_id] = summary
            self._cache_timestamps[summary_id] = datetime.now()
        
        self.logger.info(f"Generated {summary_type.name} summary: {summary_id} "
                        f"({compression_ratio:.1f}x compression)")
        
        return summary
    
    async def _generate_extractive_summary(self, turns: List[ConversationTurn]) -> str:
        """Generate extractive summary by selecting key sentences"""
        # Combine all content
        all_content = []
        for turn in turns:
            role_prefix = f"[{turn.role.upper()}]" if turn.role else "[UNKNOWN]"
            all_content.append(f"{role_prefix} {turn.content}")
        
        full_text = "\n".join(all_content)
        sentences = [s.strip() for s in full_text.split('.') if s.strip()]
        
        if len(sentences) <= 3:
            return full_text
        
        # Score sentences by length and position (simple heuristic)
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            # Prefer longer sentences and those near the beginning/end
            length_score = min(len(sentence) / 100, 1.0)
            position_score = 1.0 if i < 2 or i >= len(sentences) - 2 else 0.5
            
            total_score = length_score * position_score
            scored_sentences.append((total_score, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Select sentences to fit target token count
        selected_sentences = []
        current_tokens = 0
        target_tokens = self.config.summary_target_tokens
        
        for score, sentence in scored_sentences:
            sentence_tokens = self.token_manager.token_counter.count_tokens(sentence, include_metadata=False)
            if current_tokens + sentence_tokens <= target_tokens:
                selected_sentences.append(sentence)
                current_tokens += sentence_tokens
            
            if current_tokens >= target_tokens * 0.8:  # 80% of target
                break
        
        # Restore chronological order for selected sentences
        result_sentences = []
        for sentence in sentences:
            if sentence in selected_sentences:
                result_sentences.append(sentence)
        
        summary = ". ".join(result_sentences)
        if not summary.endswith('.'):
            summary += "."
        
        return summary
    
    async def _generate_abstractive_summary(self, turns: List[ConversationTurn]) -> str:
        """Generate abstractive summary (simplified version)"""
        # For now, this is a simplified version that creates a structured summary
        # In a full implementation, this would use an LLM for actual abstractive summarization
        
        user_messages = [t for t in turns if t.role == 'user']
        assistant_messages = [t for t in turns if t.role == 'assistant']
        
        summary_parts = []
        
        if user_messages:
            user_topics = set()
            for msg in user_messages:
                # Extract key phrases (simplified)
                words = msg.content.lower().split()
                for i in range(len(words) - 1):
                    if len(words[i]) > 3 and len(words[i+1]) > 3:
                        user_topics.add(f"{words[i]} {words[i+1]}")
            
            if user_topics:
                top_topics = list(user_topics)[:3]
                summary_parts.append(f"User discussed: {', '.join(top_topics)}")
        
        if assistant_messages:
            summary_parts.append(f"Assistant provided {len(assistant_messages)} responses")
        
        if len(turns) > 10:
            summary_parts.append(f"Extended conversation with {len(turns)} total exchanges")
        
        return ". ".join(summary_parts) + "."
    
    async def _generate_hierarchical_summary(self, turns: List[ConversationTurn]) -> str:
        """Generate hierarchical summary with multiple levels"""
        # Group turns by time periods
        time_groups = self._group_turns_by_time(turns)
        
        summary_parts = []
        for period, group_turns in time_groups.items():
            if len(group_turns) > 1:
                group_summary = await self._generate_extractive_summary(group_turns)
                # Truncate to reasonable length
                if len(group_summary) > 200:
                    group_summary = group_summary[:200] + "..."
                summary_parts.append(f"[{period}] {group_summary}")
            else:
                turn = group_turns[0]
                content = turn.content[:100] + "..." if len(turn.content) > 100 else turn.content
                summary_parts.append(f"[{period}] {turn.role}: {content}")
        
        return "\n".join(summary_parts)
    
    def _group_turns_by_time(self, turns: List[ConversationTurn]) -> Dict[str, List[ConversationTurn]]:
        """Group turns by time periods"""
        if not turns:
            return {}
        
        # Sort turns by timestamp
        sorted_turns = sorted(turns, key=lambda t: t.timestamp)
        
        groups = {}
        current_group = []
        current_period = None
        
        for turn in sorted_turns:
            # Create time period label (hour granularity)
            period = turn.timestamp.strftime("%H:00")
            
            if current_period is None:
                current_period = period
                current_group = [turn]
            elif period == current_period:
                current_group.append(turn)
            else:
                # Start new group
                if current_group:
                    groups[current_period] = current_group
                current_period = period
                current_group = [turn]
        
        # Add final group
        if current_group:
            groups[current_period] = current_group
        
        return groups
    
    def _extract_topics(self, turns: List[ConversationTurn]) -> List[str]:
        """Extract key topics from turns (simplified)"""
        word_freq = {}
        for turn in turns:
            words = turn.content.lower().split()
            for word in words:
                if len(word) > 4 and word.isalpha():
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top topics
        sorted_topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, freq in sorted_topics[:5] if freq > 1]
    
    def _extract_entities(self, turns: List[ConversationTurn]) -> List[str]:
        """Extract important entities (simplified)"""
        entities = set()
        for turn in turns:
            # Simple extraction of capitalized words (potential entities)
            words = turn.content.split()
            for word in words:
                if word[0].isupper() and len(word) > 2 and word.isalpha():
                    entities.add(word)
        
        return list(entities)[:10]  # Limit to top 10


class ContextSummarizationManager:
    """Manager for context summarization operations"""
    
    def __init__(self, config: SummaryConfig = None, storage_path: str = None):
        self.config = config or SummaryConfig()
        self.storage_path = Path(storage_path) if storage_path else Path("summaries")
        self.storage_path.mkdir(exist_ok=True)
        
        self.summarization_service = SummarizationService(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Track active summaries
        self._active_summaries: Dict[str, ConversationSummary] = {}
        
    async def process_conversation_for_summarization(self, 
                                                   turns: List[ConversationTurn],
                                                   force_summarize: bool = False) -> Tuple[List[ConversationTurn], List[ConversationSummary]]:
        """
        Process conversation turns and generate summaries as needed.
        
        Returns:
            Tuple of (remaining_turns, generated_summaries)
        """
        if not turns:
            return turns, []
        
        # Check if summarization is needed
        token_result = self.summarization_service.token_manager.count_conversation_tokens(
            [{'role': turn.role, 'content': turn.content} for turn in turns]
        )
        current_tokens = token_result.get('total_tokens', 0)
        
        should_summarize, trigger = self.summarization_service.should_summarize(
            turns, current_tokens
        )
        
        if not should_summarize and not force_summarize:
            return turns, []
        
        # Determine which turns to summarize
        preserve_count = self.config.preserve_recent_turns
        if len(turns) <= preserve_count:
            return turns, []
        
        turns_to_summarize = turns[:-preserve_count]
        turns_to_keep = turns[-preserve_count:]
        
        # Generate summary
        summary = await self.summarization_service.generate_summary(
            turns_to_summarize,
            summary_type=SummaryType.EXTRACTIVE,
            trigger=trigger or SummarizationTrigger.MANUAL
        )
        
        # Save summary
        await self._save_summary(summary)
        
        self.logger.info(f"Summarized {len(turns_to_summarize)} turns into summary {summary.summary_id}")
        
        return turns_to_keep, [summary]
    
    async def _save_summary(self, summary: ConversationSummary):
        """Save summary to storage"""
        file_path = self.storage_path / f"{summary.summary_id}.json"
        
        try:
            with open(file_path, 'w') as f:
                json.dump(summary.to_dict(), f, indent=2)
            
            self._active_summaries[summary.summary_id] = summary
            self.logger.debug(f"Saved summary to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save summary {summary.summary_id}: {e}")
    
    def _start_background_processing(self):
        """Start background thread for async summarization"""
        if self._background_thread is None or not self._background_thread.is_alive():
            self._background_thread = threading.Thread(
                target=self._background_worker,
                daemon=True
            )
            self._background_thread.start()
    
    def _background_worker(self):
        """Background worker thread for processing summarization tasks"""
        while not self._shutdown_event.is_set():
            try:
                # Get task from queue with timeout
                try:
                    task = self._background_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                if task is None:  # Shutdown signal
                    break
                
                # Process summarization task
                turns, callback = task
                try:
                    # Run summarization in executor to avoid blocking
                    future = self._background_executor.submit(
                        self._process_summarization_task, turns
                    )
                    result = future.result(timeout=30.0)  # 30 second timeout
                    
                    if callback:
                        callback(result)
                        
                except Exception as e:
                    self.logger.error(f"Background summarization failed: {e}")
                finally:
                    self._background_queue.task_done()
                    
            except Exception as e:
                self.logger.error(f"Background worker error: {e}")
    
    def _process_summarization_task(self, turns: List[ConversationTurn]) -> ConversationSummary:
        """Process a single summarization task synchronously"""
        try:
            # Use the existing generate_summary method
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                summary = loop.run_until_complete(self.generate_summary(turns))
                return summary
            finally:
                loop.close()
        except Exception as e:
            self.logger.error(f"Summarization task failed: {e}")
            raise
    
    def queue_background_summarization(self, 
                                     turns: List[ConversationTurn],
                                     callback: callable = None):
        """Queue turns for background summarization"""
        try:
            self._background_queue.put((turns, callback), timeout=0.1)
            self.logger.debug(f"Queued {len(turns)} turns for background summarization")
        except queue.Full:
            self.logger.warning("Background summarization queue is full, skipping")
    
    def shutdown(self):
        """Shutdown background processing gracefully"""
        self._shutdown_event.set()
        
        # Signal shutdown to background worker
        try:
            self._background_queue.put(None, timeout=1.0)
        except queue.Full:
            pass
        
        # Wait for background thread to finish
        if self._background_thread and self._background_thread.is_alive():
            self._background_thread.join(timeout=5.0)
        
        # Shutdown executor
        self._background_executor.shutdown(wait=True, timeout=5.0)
    
    async def load_summary(self, summary_id: str) -> Optional[ConversationSummary]:
        """Load summary from storage"""
        if summary_id in self._active_summaries:
            return self._active_summaries[summary_id]
        
        file_path = self.storage_path / f"{summary_id}.json"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            summary = ConversationSummary.from_dict(data)
            self._active_summaries[summary_id] = summary
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to load summary {summary_id}: {e}")
            return None
    
    def get_summary_statistics(self) -> Dict:
        """Get statistics about stored summaries"""
        summary_files = list(self.storage_path.glob("*.json"))
        
        stats = {
            'total_summaries': len(summary_files),
            'active_summaries': len(self._active_summaries),
            'storage_path': str(self.storage_path),
            'total_size_mb': sum(f.stat().st_size for f in summary_files) / (1024 * 1024)
        }
        
        return stats


# Global instance
_summarization_manager = None

def get_summarization_manager(config: SummaryConfig = None, 
                            storage_path: str = None) -> ContextSummarizationManager:
    """Get global summarization manager instance"""
    global _summarization_manager
    if _summarization_manager is None:
        _summarization_manager = ContextSummarizationManager(config, storage_path)
    return _summarization_manager