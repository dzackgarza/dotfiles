"""
Unified Timeline Architecture - V3.15

Single source of truth for all blocks (live and inscribed).
Eliminates dual-system architectural conflicts by making Timeline own everything.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Protocol, Any
import asyncio
from datetime import datetime, timezone

from .live_blocks import LiveBlock, InscribedBlock, BlockState
from ..widgets.timeline import TimelineBlock
from .wall_time_tracker import (
    track_block_creation,
    time_block_stage,
    complete_block_tracking,
)
from .block_audit_logger import audit_logger, OperationType
from .context_formatting import context_formatting_manager, FormatStyle


class TimelineEvent:
    """Base class for timeline events"""

    pass


@dataclass
class BlockAdded(TimelineEvent):
    """Event fired when a block is added to timeline"""

    block: Union[LiveBlock, InscribedBlock]


@dataclass
class BlockUpdated(TimelineEvent):
    """Event fired when a block is updated"""

    block: Union[LiveBlock, InscribedBlock]


@dataclass
class BlockInscribed(TimelineEvent):
    """Event fired when a live block becomes inscribed"""

    inscribed_block: InscribedBlock
    original_live_id: str


class TimelineObserver(Protocol):
    """Protocol for timeline observers"""

    def on_timeline_event(self, event: TimelineEvent) -> None:
        """Handle timeline events"""
        ...


class UnifiedTimeline:
    """Single timeline that handles both live and inscribed blocks

    This eliminates the fundamental ownership conflict between LiveBlockManager
    and Timeline by making Timeline the single source of truth for all blocks.

    Architecture:
    - Timeline owns all blocks (live and inscribed)
    - LiveBlockManager becomes a pure factory (no ownership)
    - Atomic inscription preserves complete block structures
    - Single widget tree matches timeline structure
    """

    def __init__(self):
        # Single list containing both live and inscribed blocks
        self._blocks: List[Union[LiveBlock, InscribedBlock]] = []

        # Observer pattern for UI updates
        self._observers: List[TimelineObserver] = []

        # Index for fast lookup
        self._block_index: Dict[str, Union[LiveBlock, InscribedBlock]] = {}

        # State tracking
        self._inscription_lock = asyncio.Lock()

    def add_observer(self, observer: TimelineObserver) -> None:
        """Add observer for timeline events"""
        self._observers.append(observer)

    def remove_observer(self, observer: TimelineObserver) -> None:
        """Remove observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, event: TimelineEvent) -> None:
        """Notify all observers of timeline event"""
        for observer in self._observers:
            try:
                observer.on_timeline_event(event)
            except Exception as e:
                print(f"Error in timeline observer: {e}")

    def add_live_block(self, role: str, content: str = "") -> LiveBlock:
        """Create and add a live block to timeline

        The block is immediately added to the timeline in live state.
        UI can show it with live styling while it updates.
        """
        # Start audit tracking for block creation
        operation_id = audit_logger.start_operation(
            block_id="pending",  # Will update once we have block ID
            operation_type=OperationType.CREATION,
            user_context=f"role={role}",
            initial_content_length=len(content)
        )
        
        try:
            # Time the block creation process
            with time_block_stage("timeline_creation", "creation"):
                block = LiveBlock(role, content)

                # Update audit log with actual block ID
                audit_logger.log_performance_metric(
                    block_id=block.id,
                    operation_type=OperationType.CREATION,
                    metrics={"content_length": len(content)},
                    operation_id=operation_id
                )

                # Add to timeline immediately
                self._blocks.append(block)
                self._block_index[block.id] = block

                # Set up callback to notify observers when block updates
                block.add_update_callback(self._on_live_block_update)

            # Notify observers
            self._notify_observers(BlockAdded(block))
            
            # Complete audit tracking
            audit_logger.end_operation(
                operation_id, 
                success=True,
                result_data={
                    "block_id": block.id,
                    "role": role,
                    "content_length": len(content),
                    "total_blocks": len(self._blocks)
                }
            )

            return block
            
        except Exception as e:
            # Log error in audit trail
            audit_logger.log_error(
                block_id="creation_failed",
                operation_type=OperationType.CREATION,
                message=f"Failed to create live block: {str(e)}",
                exception=e,
                operation_id=operation_id
            )
            audit_logger.end_operation(operation_id, success=False)
            raise

    def _on_live_block_update(self, block: LiveBlock) -> None:
        """Handle live block updates with context management integration"""
        # Log block modification
        operation_id = audit_logger.start_operation(
            block_id=block.id,
            operation_type=OperationType.MODIFICATION,
            user_context="live_block_update"
        )
        
        try:
            # Check if this update should trigger context summarization
            self._check_context_triggers_on_update(block)
            
            # Notify observers of the update
            self._notify_observers(BlockUpdated(block))
            
            # Log successful update with context awareness
            audit_logger.log_performance_metric(
                block_id=block.id,
                operation_type=OperationType.MODIFICATION,
                metrics={
                    "content_length": len(block.content),
                    "observer_count": len(self._observers),
                    "total_timeline_blocks": len(self._blocks),
                    "total_inscribed_blocks": len(self.get_inscribed_blocks())
                },
                operation_id=operation_id
            )
            
            audit_logger.end_operation(operation_id, success=True)
            
        except Exception as e:
            audit_logger.log_error(
                block_id=block.id,
                operation_type=OperationType.MODIFICATION,
                message=f"Failed to handle live block update: {str(e)}",
                exception=e,
                operation_id=operation_id
            )
            audit_logger.end_operation(operation_id, success=False)
    
    def _check_context_triggers_on_update(self, updated_block: LiveBlock) -> None:
        """Check if block updates should trigger context management actions"""
        try:
            # Check if we have too many blocks (trigger summarization)
            total_blocks = len(self._blocks)
            if total_blocks > 20:  # Configurable threshold
                # Schedule background summarization
                asyncio.create_task(self._background_summarization())
            
            # Check if the updated block is large (might need special handling)
            content_length = len(updated_block.content)
            if content_length > 5000:  # Large block threshold
                audit_logger.log_performance_metric(
                    block_id=updated_block.id,
                    operation_type=OperationType.MODIFICATION,
                    metrics={
                        "large_block_detected": True,
                        "content_length": content_length,
                        "recommendation": "consider_chunking"
                    }
                )
                
        except Exception as e:
            # Don't fail the update due to context check issues
            print(f"Warning: Context trigger check failed: {e}")
    
    async def _background_summarization(self) -> None:
        """Perform background summarization when timeline grows large"""
        try:
            from .summarization import ContextSummarizationManager, SummaryConfig
            
            # Get current inscribed blocks for summarization
            inscribed_blocks = self.get_inscribed_blocks()
            if len(inscribed_blocks) < 5:  # Need minimum blocks for summarization
                return
            
            # Convert to conversation turns
            from .context_scoring import ConversationTurn
            from datetime import datetime, timezone
            
            turns = []
            for block in inscribed_blocks[:-3]:  # Keep last 3 blocks, summarize older ones
                role = self._determine_block_role(block)
                turn = ConversationTurn(
                    id=block.id,
                    content=block.content,
                    role=role,
                    timestamp=self._get_block_timestamp(block),
                    tokens=len(block.content.split()) * 1.3
                )
                turns.append(turn)
            
            if turns:
                # Configure summarization for background processing
                config = SummaryConfig(
                    max_context_tokens=2000,
                    summary_target_tokens=400,
                    preserve_recent_turns=0  # We already filtered to older blocks
                )
                
                summarization_manager = ContextSummarizationManager(config=config)
                remaining_turns, summaries = await summarization_manager.process_conversation_for_summarization(
                    turns, force_summarize=True
                )
                
                if summaries:
                    # Log successful background summarization
                    audit_logger.log_performance_metric(
                        block_id="timeline_background_summarization",
                        operation_type=OperationType.MODIFICATION,
                        metrics={
                            "original_blocks": len(turns),
                            "summaries_created": len(summaries),
                            "storage_reduction": f"{len(turns) - len(remaining_turns)} blocks summarized"
                        }
                    )
                    
        except Exception as e:
            audit_logger.log_error(
                block_id="timeline_background_summarization",
                operation_type=OperationType.MODIFICATION,
                message=f"Background summarization failed: {str(e)}",
                exception=e
            )

    def get_block(self, block_id: str) -> Optional[Union[LiveBlock, InscribedBlock]]:
        """Get block by ID"""
        return self._block_index.get(block_id)

    def owns_block(self, block_id: str) -> bool:
        """Check if timeline owns this block"""
        return block_id in self._block_index

    def get_all_blocks(self) -> List[Union[LiveBlock, InscribedBlock]]:
        """Get all blocks in timeline order"""
        return self._blocks.copy()

    def get_live_blocks(self) -> List[LiveBlock]:
        """Get only live blocks"""
        return [block for block in self._blocks if isinstance(block, LiveBlock)]

    def get_inscribed_blocks(self) -> List[InscribedBlock]:
        """Get only inscribed blocks"""
        return [block for block in self._blocks if isinstance(block, InscribedBlock)]

    async def inscribe_block(self, block_id: str, force: bool = False) -> Optional[InscribedBlock]:
        """Atomically convert live block to inscribed, including all sub-blocks

        This is the critical method that fixes the ownership conflicts.
        It converts the complete live block tree to inscribed state atomically.
        Now includes comprehensive validation and error handling.
        
        Args:
            block_id: ID of the block to inscribe
            force: Skip validation checks if True (use with caution)
        """
        from .block_state_transitions import transition_manager, ValidationError, InscriptionError
        
        # Start audit tracking for inscription
        operation_id = audit_logger.start_operation(
            block_id=block_id,
            operation_type=OperationType.STATE_TRANSITION,
            user_context=f"inscribe_block(force={force})"
        )
        
        async with self._inscription_lock:
            # Find the live block
            live_block = self._block_index.get(block_id)
            if not live_block or not isinstance(live_block, LiveBlock):
                audit_logger.log_error(
                    block_id=block_id,
                    operation_type=OperationType.STATE_TRANSITION,
                    message=f"Block not found or not live: {block_id}",
                    operation_id=operation_id
                )
                audit_logger.end_operation(operation_id, success=False)
                return None

            try:
                # Log pre-inscription state
                audit_logger.log_integrity_check(
                    block_id=block_id,
                    check_results={
                        "block_exists": True,
                        "is_live": isinstance(live_block, LiveBlock),
                        "has_content": bool(live_block.content),
                        "in_timeline": block_id in self._block_index
                    },
                    data_snapshot={
                        "content_length": len(live_block.content),
                        "role": live_block.role,
                        "state": str(live_block.state)
                    },
                    operation_id=operation_id
                )
                
                # Use the new transition manager for safe inscription
                inscribed_block = await transition_manager.transition_to_inscribed(
                    block=live_block,
                    force=force,
                    auto_recover=True
                )
                
                if not inscribed_block:
                    audit_logger.log_error(
                        block_id=block_id,
                        operation_type=OperationType.STATE_TRANSITION,
                        message="Transition manager failed to create inscribed block",
                        operation_id=operation_id
                    )
                    audit_logger.end_operation(operation_id, success=False)
                    return None

                # Atomic replacement in timeline
                block_index = self._blocks.index(live_block)
                self._blocks[block_index] = inscribed_block

                # Update index
                del self._block_index[block_id]
                self._block_index[inscribed_block.id] = inscribed_block

                # Notify observers
                self._notify_observers(BlockInscribed(inscribed_block, block_id))
                
                # Log successful inscription with final state
                audit_logger.log_state_transition(
                    block_id=block_id,
                    from_state="LIVE",
                    to_state="INSCRIBED",
                    operation_id=operation_id,
                    validation_results={
                        "inscription_successful": True,
                        "content_preserved": inscribed_block.content == live_block.content,
                        "timeline_updated": inscribed_block.id in self._block_index
                    }
                )
                
                audit_logger.end_operation(
                    operation_id,
                    success=True,
                    result_data={
                        "inscribed_block_id": inscribed_block.id,
                        "original_block_id": block_id,
                        "content_length": len(inscribed_block.content),
                        "timeline_position": self._blocks.index(inscribed_block)
                    }
                )

                return inscribed_block
                
            except (ValidationError, InscriptionError) as e:
                audit_logger.log_error(
                    block_id=block_id,
                    operation_type=OperationType.STATE_TRANSITION,
                    message=f"Validation/Inscription error: {str(e)}",
                    exception=e,
                    operation_id=operation_id
                )
                audit_logger.end_operation(operation_id, success=False)
                print(f"Failed to inscribe block {block_id}: {e}")
                # Block remains in live state
                return None
            except Exception as e:
                audit_logger.log_error(
                    block_id=block_id,
                    operation_type=OperationType.STATE_TRANSITION,
                    message=f"Unexpected error during inscription: {str(e)}",
                    exception=e,
                    operation_id=operation_id
                )
                audit_logger.end_operation(operation_id, success=False)
                print(f"Unexpected error inscribing block {block_id}: {e}")
                return None

    async def validate_block_for_inscription(self, block_id: str) -> Optional[Dict[str, Any]]:
        """Validate if a block is ready for inscription.
        
        Returns:
            Dictionary with validation results, or None if block not found
        """
        from .block_state_transitions import transition_manager
        
        live_block = self._block_index.get(block_id)
        if not live_block or not isinstance(live_block, LiveBlock):
            return None
        
        try:
            validation_result = await transition_manager.validate_transition(
                live_block, 
                BlockState.INSCRIBED
            )
            
            return {
                'is_valid': validation_result.is_valid,
                'failed_conditions': [c.value for c in validation_result.failed_conditions],
                'errors': validation_result.error_messages,
                'warnings': validation_result.warnings,
                'block_id': block_id
            }
        except Exception as e:
            return {
                'is_valid': False,
                'failed_conditions': [],
                'errors': [f"Validation error: {e}"],
                'warnings': [],
                'block_id': block_id
            }

    def get_blocks_ready_for_inscription(self) -> List[str]:
        """Get IDs of live blocks that appear ready for inscription.
        
        This is a synchronous check based on basic conditions.
        Use validate_block_for_inscription() for comprehensive async validation.
        """
        ready_block_ids = []
        
        for block in self.get_live_blocks():
            # Basic readiness checks
            if (block.data.progress >= 1.0 and 
                block.data.content.strip() and
                not block._is_simulating and
                block.state == BlockState.LIVE):
                ready_block_ids.append(block.id)
        
        return ready_block_ids

    async def get_formatted_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL, 
                                  max_tokens: int = 4000, query: str = None) -> str:
        """
        Get formatted conversation context from inscribed blocks with optional summarization.
        
        Enhanced integration with context management system providing:
        - Accurate token counting via ConversationTokenManager
        - Smart context selection based on relevance to current query
        - Automatic summarization when context exceeds limits
        - Proper timeline-to-conversation-turn conversion
        
        Args:
            format_style: How to format the context (conversational, technical, etc.)
            max_tokens: Maximum tokens to include in context
            query: Current query for relevance scoring (optional)
        """
        from .context_scoring import ConversationTurn, advanced_context_scorer
        from .token_counter import ConversationTokenManager
        from .summarization import ContextSummarizationManager, SummaryConfig
        from datetime import datetime, timezone
        
        # Initialize enhanced context management components
        token_manager = ConversationTokenManager()
        summary_config = SummaryConfig(
            max_context_tokens=max_tokens,
            summary_target_tokens=max_tokens // 4,  # 25% of available space for summaries
            preserve_recent_turns=3  # Always keep last 3 turns
        )
        summarization_manager = ContextSummarizationManager(config=summary_config)
        
        # Convert timeline blocks to conversation turns with proper metadata
        turns = []
        for block in self.get_inscribed_blocks():
            # Enhanced role detection from block metadata
            role = self._determine_block_role(block)
            
            # Get accurate token count using token manager
            token_count = token_manager.token_counter.count_tokens(block.content)
            actual_tokens = token_count.get('total_tokens', len(block.content.split()) * 1.3)
            
            # Create conversation turn with complete metadata
            turn = ConversationTurn(
                id=block.id,
                content=block.content,
                role=role,
                timestamp=self._get_block_timestamp(block),
                tokens=actual_tokens,
                metadata={
                    'block_type': 'inscribed',
                    'original_metadata': getattr(block, 'metadata', {}),
                    'wall_time_seconds': getattr(block, 'metadata', {}).get('wall_time_seconds'),
                    'tokens_input': getattr(block, 'metadata', {}).get('tokens_input'),
                    'tokens_output': getattr(block, 'metadata', {}).get('tokens_output')
                }
            )
            turns.append(turn)
        
        # Handle empty timeline
        if not turns:
            return "--- No conversation history available ---"
            
        # Apply intelligent context selection and summarization
        if len(turns) > 1:
            # Check if summarization is needed
            total_tokens = sum(turn.tokens for turn in turns)
            if total_tokens > max_tokens:
                # Process with summarization
                remaining_turns, summaries = await summarization_manager.process_conversation_for_summarization(
                    turns, force_summarize=True
                )
                selected_turns = remaining_turns
                
                # Log summarization for timeline audit
                if summaries:
                    audit_logger.log_performance_metric(
                        block_id="timeline_context",
                        operation_type=OperationType.MODIFICATION,
                        metrics={
                            'original_turns': len(turns),
                            'summarized_turns': len(selected_turns),
                            'summaries_generated': len(summaries),
                            'compression_ratio': summaries[0].metadata.compression_ratio if summaries else 1.0
                        }
                    )
            else:
                # Use context scoring for optimal selection
                query_text = query or "current conversation context"
                selected_turns = advanced_context_scorer.get_optimal_context(
                    turns,
                    query_text,
                    max_tokens=max_tokens
                )
        else:
            selected_turns = turns
            
        # Apply enhanced formatting with timeline context
        from .context_formatting import FormatSettings
        settings = FormatSettings(
            style=format_style,
            include_metadata=True,
            enable_summarization=True,
            max_context_tokens=max_tokens,
            summarization_config=summary_config
        )
        
        formatted_result = await context_formatting_manager.format_context(
            selected_turns, 
            format_style,
            settings
        )
        
        # Update timeline metadata with context usage
        self._update_context_usage_metadata(formatted_result)
        
        return formatted_result.formatted_text
    
    async def get_live_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL, 
                             max_tokens: int = 2000, query: str = None) -> str:
        """
        Get formatted context from currently active live blocks.
        
        This provides context from ongoing conversations/work that hasn't been
        inscribed yet, useful for real-time context during live interactions.
        """
        from .context_scoring import ConversationTurn
        from .token_counter import ConversationTokenManager
        from datetime import datetime, timezone
        
        # Initialize token manager for accurate counting
        token_manager = ConversationTokenManager()
        
        # Convert live blocks to conversation turns
        turns = []
        for block in self.get_live_blocks():
            # Only include blocks with meaningful content
            if not block.content.strip():
                continue
                
            role = self._determine_block_role(block)
            
            # Get accurate token count
            token_count = token_manager.token_counter.count_tokens(block.content)
            actual_tokens = token_count.get('total_tokens', len(block.content.split()) * 1.3)
            
            turn = ConversationTurn(
                id=block.id,
                content=block.content,
                role=role,
                timestamp=getattr(block, 'created_at', datetime.now(timezone.utc)),
                tokens=actual_tokens,
                metadata={
                    'block_type': 'live',
                    'progress': getattr(block.data, 'progress', 0.0),
                    'is_simulating': getattr(block, '_is_simulating', False),
                    'wall_time_seconds': getattr(block.data, 'wall_time_seconds', 0)
                }
            )
            turns.append(turn)
        
        if not turns:
            return "--- No active live blocks ---"
        
        # Apply context selection if needed
        if len(turns) > 1 and query:
            from .context_scoring import advanced_context_scorer
            selected_turns = advanced_context_scorer.get_optimal_context(
                turns, query, max_tokens=max_tokens
            )
        else:
            # Keep all live turns but respect token limit
            total_tokens = sum(turn.tokens for turn in turns)
            if total_tokens > max_tokens:
                # Take most recent turns that fit
                selected_turns = []
                current_tokens = 0
                for turn in reversed(turns):
                    if current_tokens + turn.tokens <= max_tokens:
                        selected_turns.insert(0, turn)
                        current_tokens += turn.tokens
                    else:
                        break
            else:
                selected_turns = turns
        
        # Format the live context
        from .context_formatting import FormatSettings
        settings = FormatSettings(
            style=format_style,
            include_metadata=True,
            enable_summarization=False,  # Don't summarize live content
            max_context_tokens=max_tokens
        )
        
        formatted_result = await context_formatting_manager.format_context(
            selected_turns, format_style, settings
        )
        
        return formatted_result.formatted_text
    
    async def get_complete_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL,
                                 max_tokens: int = 6000, query: str = None,
                                 include_live: bool = True) -> str:
        """
        Get complete conversation context combining inscribed and live blocks.
        
        This provides the full timeline context, intelligently managed with
        summarization and context scoring to fit within token limits.
        """
        # Allocate tokens between inscribed and live content
        if include_live:
            inscribed_tokens = int(max_tokens * 0.7)  # 70% for inscribed history
            live_tokens = int(max_tokens * 0.3)       # 30% for live content
        else:
            inscribed_tokens = max_tokens
            live_tokens = 0
        
        # Get inscribed context (historical conversation)
        inscribed_context = await self.get_formatted_context(
            format_style=format_style,
            max_tokens=inscribed_tokens,
            query=query
        )
        
        # Get live context if requested
        if include_live and live_tokens > 0:
            live_context = await self.get_live_context(
                format_style=format_style,
                max_tokens=live_tokens,
                query=query
            )
        else:
            live_context = ""
        
        # Combine contexts with appropriate separators
        if format_style == FormatStyle.TECHNICAL:
            separator = "\n\n=== LIVE BLOCKS ===\n"
        elif format_style == FormatStyle.STRUCTURED:
            separator = "\n\n## Current Live Blocks\n"
        else:  # CONVERSATIONAL
            separator = "\n\n--- Current Activity ---\n"
        
        if live_context and not live_context.startswith("--- No active"):
            complete_context = inscribed_context + separator + live_context
        else:
            complete_context = inscribed_context
        
        # Log complete context generation
        audit_logger.log_performance_metric(
            block_id="timeline_complete_context",
            operation_type=OperationType.QUERY,
            metrics={
                'inscribed_length': len(inscribed_context),
                'live_length': len(live_context),
                'total_length': len(complete_context),
                'format_style': format_style.value if hasattr(format_style, 'value') else str(format_style),
                'token_allocation': f"{inscribed_tokens}/{live_tokens}",
                'query_provided': bool(query)
            }
        )
        
        return complete_context
    
    def _determine_block_role(self, block) -> str:
        """Enhanced role detection from block metadata"""
        # Check explicit role field
        if hasattr(block, 'role') and block.role:
            return block.role
            
        # Check metadata for role hints
        metadata = getattr(block, 'metadata', {})
        if 'role' in metadata:
            return metadata['role']
            
        # Heuristic based on content patterns
        content = block.content.strip().lower()
        if content.startswith(('hello', 'hi', 'help', 'how', 'what', 'why', 'when', 'where')):
            return 'user'
        elif content.startswith(('i can', 'let me', 'here\'s', 'to do this', 'the solution')):
            return 'assistant'
            
        # Default fallback - alternate between user and assistant
        # This could be enhanced with more sophisticated detection
        return 'user'  # Conservative default
    
    def _get_block_timestamp(self, block) -> datetime:
        """Get proper timestamp from block with fallbacks"""
        # Try different timestamp fields
        for attr in ['timestamp', 'created_at', 'inscribed_at']:
            if hasattr(block, attr):
                ts = getattr(block, attr)
                if isinstance(ts, datetime):
                    return ts
                    
        # Check metadata
        metadata = getattr(block, 'metadata', {})
        if 'created_at' in metadata:
            try:
                return datetime.fromisoformat(metadata['created_at'])
            except (ValueError, TypeError):
                pass
                
        # Fallback to current time
        return datetime.now(timezone.utc)
    
    def _update_context_usage_metadata(self, formatted_result) -> None:
        """Update timeline metadata with context usage statistics"""
        try:
            # Store context usage metrics in timeline metadata
            # This helps track how context management is performing
            usage_stats = {
                'last_context_generation': datetime.now(timezone.utc).isoformat(),
                'context_length': len(formatted_result.formatted_text),
                'total_tokens': formatted_result.total_tokens,
                'turns_included': formatted_result.turn_count,
                'summaries_used': len(formatted_result.summaries_used) if hasattr(formatted_result, 'summaries_used') else 0
            }
            
            # This could be stored in a timeline-level metadata store
            # For now, we log it for audit purposes
            audit_logger.log_performance_metric(
                block_id="timeline_context_usage",
                operation_type=OperationType.QUERY,
                metrics=usage_stats
            )
        except Exception as e:
            # Don't fail context generation due to metadata issues
            print(f"Warning: Could not update context usage metadata: {e}")

    def add_sub_block(
        self, parent_id: str, role: str, content: str = ""
    ) -> Optional[LiveBlock]:
        """Add sub-block to existing live block

        Sub-blocks are owned by their parent - they never exist independently.
        This prevents the orphaned sub-block problem.
        """
        parent_block = self._block_index.get(parent_id)
        if not parent_block or not isinstance(parent_block, LiveBlock):
            return None

        # Create sub-block
        sub_block = LiveBlock(role, content)

        # Add to parent (parent owns it, not timeline)
        parent_block.add_sub_block(sub_block)

        # Sub-blocks are NOT added to timeline index - parent owns them
        # This prevents duplicate rendering and ownership conflicts

        return sub_block

    def clear_all_live_blocks(self) -> None:
        """Stop all live block simulations"""
        for block in self.get_live_blocks():
            block.stop_simulation()

    def to_timeline_blocks(self) -> List[TimelineBlock]:
        """Convert to legacy TimelineBlock format for compatibility

        This allows gradual migration from old timeline system.
        """
        timeline_blocks = []

        for block in self._blocks:
            if isinstance(block, InscribedBlock):
                # Convert inscribed block
                timeline_block = TimelineBlock(
                    id=block.id,
                    timestamp=block.timestamp,
                    role=block.role,
                    content=block.content,
                    metadata=block.metadata.copy(),
                    time_taken=block.metadata.get("wall_time_seconds"),
                    tokens_input=block.metadata.get("tokens_input"),
                    tokens_output=block.metadata.get("tokens_output"),
                    sub_blocks=[],  # Sub-blocks are in metadata for inscribed blocks
                )
                timeline_blocks.append(timeline_block)

            elif isinstance(block, LiveBlock):
                # Convert live block (for current display)
                timeline_block = TimelineBlock(
                    id=block.id,
                    timestamp=block.created_at,
                    role=block.role,
                    content=block.data.content,
                    metadata=block.data.metadata.copy(),
                    time_taken=block.data.wall_time_seconds,
                    tokens_input=block.data.tokens_input,
                    tokens_output=block.data.tokens_output,
                    sub_blocks=[],  # Live sub-blocks handled separately
                )
                timeline_blocks.append(timeline_block)

        return timeline_blocks


class UnifiedTimelineManager:
    """Enhanced timeline manager with integrated context management capabilities
    
    This replaces LiveBlockManager with clear ownership boundaries and provides
    a complete context management interface for the Sacred Timeline.
    """

    def __init__(self):
        self.timeline = UnifiedTimeline()

    def create_live_block(self, role: str, initial_content: str = "") -> LiveBlock:
        """Create live block - delegates to timeline for ownership"""
        return self.timeline.add_live_block(role, initial_content)

    def add_sub_block(
        self, parent_id: str, role: str, content: str = ""
    ) -> Optional[LiveBlock]:
        """Add sub-block to parent - delegates to timeline"""
        return self.timeline.add_sub_block(parent_id, role, content)

    async def inscribe_block(self, block_id: str) -> Optional[InscribedBlock]:
        """Inscribe block - delegates to timeline"""
        return await self.timeline.inscribe_block(block_id)

    def get_timeline(self) -> UnifiedTimeline:
        """Get the unified timeline"""
        return self.timeline

    def stop_all_simulations(self) -> None:
        """Stop all live simulations"""
        self.timeline.clear_all_live_blocks()
    
    # Enhanced Context Management Interface
    
    async def get_conversation_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL,
                                     max_tokens: int = 4000, query: str = None) -> str:
        """Get formatted conversation context with intelligent management"""
        return await self.timeline.get_formatted_context(format_style, max_tokens, query)
    
    async def get_live_conversation_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL,
                                          max_tokens: int = 2000, query: str = None) -> str:
        """Get context from currently active live blocks"""
        return await self.timeline.get_live_context(format_style, max_tokens, query)
    
    async def get_complete_conversation_context(self, format_style: FormatStyle = FormatStyle.CONVERSATIONAL,
                                              max_tokens: int = 6000, query: str = None,
                                              include_live: bool = True) -> str:
        """Get complete conversation context combining all blocks"""
        return await self.timeline.get_complete_context(format_style, max_tokens, query, include_live)
    
    def get_context_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current timeline and context state"""
        inscribed_blocks = self.timeline.get_inscribed_blocks()
        live_blocks = self.timeline.get_live_blocks()
        
        # Calculate content statistics
        total_inscribed_content = sum(len(block.content) for block in inscribed_blocks)
        total_live_content = sum(len(block.content) for block in live_blocks)
        
        return {
            'total_blocks': len(self.timeline._blocks),
            'inscribed_blocks': len(inscribed_blocks),
            'live_blocks': len(live_blocks),
            'total_inscribed_characters': total_inscribed_content,
            'total_live_characters': total_live_content,
            'estimated_inscribed_tokens': total_inscribed_content * 0.75,  # Rough estimate
            'estimated_live_tokens': total_live_content * 0.75,
            'blocks_ready_for_inscription': len(self.timeline.get_blocks_ready_for_inscription()),
            'context_management_active': True
        }
    
    async def optimize_timeline_context(self, target_tokens: int = 4000) -> Dict[str, Any]:
        """Optimize timeline for better context management
        
        Returns summary of optimization actions taken.
        """
        optimization_results = {
            'actions_taken': [],
            'before_stats': self.get_context_statistics(),
            'summarization_triggered': False,
            'blocks_inscribed': 0
        }
        
        # Check if we should inscribe ready blocks
        ready_blocks = self.timeline.get_blocks_ready_for_inscription()
        if ready_blocks:
            for block_id in ready_blocks[:5]:  # Limit to 5 at a time
                inscribed = await self.timeline.inscribe_block(block_id)
                if inscribed:
                    optimization_results['blocks_inscribed'] += 1
                    optimization_results['actions_taken'].append(f'inscribed_block_{block_id}')
        
        # Check if we should trigger summarization
        stats = self.get_context_statistics()
        if stats['estimated_inscribed_tokens'] > target_tokens * 2:
            # Trigger background summarization
            await self.timeline._background_summarization()
            optimization_results['summarization_triggered'] = True
            optimization_results['actions_taken'].append('background_summarization')
        
        optimization_results['after_stats'] = self.get_context_statistics()
        
        # Log optimization results
        audit_logger.log_performance_metric(
            block_id="timeline_optimization",
            operation_type=OperationType.MODIFICATION,
            metrics=optimization_results
        )
        
        return optimization_results
