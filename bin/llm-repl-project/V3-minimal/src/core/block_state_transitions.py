"""
Block State Transition Logic with Error Handling

This module implements comprehensive state transition logic for blocks,
including validation, error handling, and recovery mechanisms.
"""

import asyncio
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union, Callable, Any
from contextlib import asynccontextmanager

from .live_blocks import LiveBlock, InscribedBlock, BlockState
from .block_metadata import ProcessingStage, BlockRole
from .wall_time_tracker import complete_block_tracking


class TransitionError(Exception):
    """Base exception for state transition errors."""
    pass


class InscriptionError(TransitionError):
    """Specific error during block inscription process."""
    pass


class ValidationError(TransitionError):
    """Error during pre-transition validation."""
    pass


class RecoveryError(TransitionError):
    """Error during transition recovery attempt."""
    pass


class TransitionCondition(Enum):
    """Conditions that must be met for state transitions."""
    CONTENT_COMPLETE = "content_complete"
    TOKENS_FINALIZED = "tokens_finalized"
    SUB_BLOCKS_READY = "sub_blocks_ready"
    PROCESSING_FINISHED = "processing_finished"
    METADATA_VALID = "metadata_valid"
    RESOURCES_AVAILABLE = "resources_available"
    NO_ACTIVE_OPERATIONS = "no_active_operations"


@dataclass
class TransitionValidationResult:
    """Result of transition validation check."""
    is_valid: bool
    failed_conditions: List[TransitionCondition] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def has_errors(self) -> bool:
        return not self.is_valid or len(self.error_messages) > 0
    
    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


@dataclass
class TransitionState:
    """Tracks the state of an ongoing transition."""
    block_id: str
    from_state: BlockState
    to_state: BlockState
    started_at: datetime
    attempt_count: int = 0
    last_error: Optional[Exception] = None
    rollback_data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_seconds(self) -> float:
        return (datetime.now() - self.started_at).total_seconds()


class TransitionValidator(ABC):
    """Abstract base for transition validation strategies."""
    
    @abstractmethod
    async def validate(self, block: LiveBlock) -> TransitionValidationResult:
        """Validate if block is ready for transition."""
        pass


class PreInscriptionValidator(TransitionValidator):
    """Validates blocks are ready for inscription to timeline."""
    
    async def validate(self, block: LiveBlock) -> TransitionValidationResult:
        """Comprehensive pre-inscription validation."""
        failed_conditions = []
        error_messages = []
        warnings = []
        
        # Check content completeness
        if not block.data.content.strip():
            failed_conditions.append(TransitionCondition.CONTENT_COMPLETE)
            error_messages.append("Block content is empty or whitespace only")
        
        # Check token finalization
        if block.data.tokens_input < 0 or block.data.tokens_output < 0:
            failed_conditions.append(TransitionCondition.TOKENS_FINALIZED)
            error_messages.append("Token counts are negative or uninitialized")
        
        # Check sub-blocks readiness
        for sub_block in block.data.sub_blocks:
            if sub_block.state == BlockState.LIVE and sub_block.data.progress < 1.0:
                failed_conditions.append(TransitionCondition.SUB_BLOCKS_READY)
                error_messages.append(f"Sub-block {sub_block.id} is not complete (progress: {sub_block.data.progress})")
        
        # Check processing status
        if hasattr(block.data, 'processing_stage'):
            stage = block.data.processing_stage
            if stage not in [ProcessingStage.COMPLETED, ProcessingStage.INSCRIBED]:
                failed_conditions.append(TransitionCondition.PROCESSING_FINISHED)
                error_messages.append(f"Block processing not finished (stage: {stage.value})")
        
        # Check metadata validity
        required_metadata = ['role', 'created_at']
        for field in required_metadata:
            if field not in block.data.metadata:
                failed_conditions.append(TransitionCondition.METADATA_VALID)
                error_messages.append(f"Missing required metadata field: {field}")
        
        # Check for active operations
        if block._is_simulating:
            failed_conditions.append(TransitionCondition.NO_ACTIVE_OPERATIONS)
            error_messages.append("Block has active simulation running")
        
        # Warnings for potentially problematic states
        if block.data.wall_time_seconds == 0:
            warnings.append("Wall time is zero - may indicate timing issue")
        
        if block.data.tokens_input == 0 and block.role != BlockRole.USER:
            warnings.append("Input token count is zero for non-user block")
        
        is_valid = len(failed_conditions) == 0
        
        return TransitionValidationResult(
            is_valid=is_valid,
            failed_conditions=failed_conditions,
            error_messages=error_messages,
            warnings=warnings
        )


class TransitionRecoveryStrategy(ABC):
    """Abstract base for transition recovery strategies."""
    
    @abstractmethod
    async def recover(self, transition_state: TransitionState, block: LiveBlock) -> bool:
        """Attempt to recover from transition failure."""
        pass


class StandardRecoveryStrategy(TransitionRecoveryStrategy):
    """Standard recovery strategy with common patterns."""
    
    async def recover(self, transition_state: TransitionState, block: LiveBlock) -> bool:
        """Attempt standard recovery operations."""
        try:
            # Stop any running operations
            if block._is_simulating:
                block.stop_simulation()
                await asyncio.sleep(0.1)  # Allow cleanup
            
            # Reset progress if needed
            if block.data.progress < 1.0:
                block.set_progress(1.0)
            
            # Finalize token counts if invalid
            if block.data.tokens_input < 0:
                block.set_tokens(0, max(0, block.data.tokens_output))
            if block.data.tokens_output < 0:
                block.set_tokens(max(0, block.data.tokens_input), 0)
            
            # Complete wall time tracking
            complete_block_tracking(block.id)
            
            return True
            
        except Exception as e:
            print(f"Recovery failed for block {block.id}: {e}")
            return False


class BlockTransitionManager:
    """Manages block state transitions with validation and error handling."""
    
    def __init__(self):
        self._active_transitions: Dict[str, TransitionState] = {}
        self._transition_lock = threading.RLock()
        self._validators: Dict[str, TransitionValidator] = {
            'pre_inscription': PreInscriptionValidator()
        }
        self._recovery_strategies: List[TransitionRecoveryStrategy] = [
            StandardRecoveryStrategy()
        ]
        self._max_retry_attempts = 3
        self._transition_callbacks: List[Callable[[TransitionState], None]] = []
    
    def add_transition_callback(self, callback: Callable[[TransitionState], None]) -> None:
        """Add callback for transition state changes."""
        self._transition_callbacks.append(callback)
    
    def _notify_transition_callbacks(self, transition_state: TransitionState) -> None:
        """Notify all registered callbacks of transition state change."""
        for callback in self._transition_callbacks:
            try:
                callback(transition_state)
            except Exception as e:
                print(f"Error in transition callback: {e}")
    
    @asynccontextmanager
    async def transition_context(self, block: LiveBlock, to_state: BlockState):
        """Context manager for safe state transitions."""
        transition_state = TransitionState(
            block_id=block.id,
            from_state=block.state,
            to_state=to_state,
            started_at=datetime.now()
        )
        
        with self._transition_lock:
            self._active_transitions[block.id] = transition_state
        
        try:
            self._notify_transition_callbacks(transition_state)
            yield transition_state
        except Exception as e:
            transition_state.last_error = e
            transition_state.attempt_count += 1
            self._notify_transition_callbacks(transition_state)
            raise
        finally:
            with self._transition_lock:
                if block.id in self._active_transitions:
                    del self._active_transitions[block.id]
    
    async def validate_transition(
        self, 
        block: LiveBlock, 
        to_state: BlockState,
        validator_name: str = 'pre_inscription'
    ) -> TransitionValidationResult:
        """Validate if block is ready for state transition."""
        if validator_name not in self._validators:
            raise ValueError(f"Unknown validator: {validator_name}")
        
        validator = self._validators[validator_name]
        return await validator.validate(block)
    
    async def transition_to_inscribed(
        self, 
        block: LiveBlock,
        force: bool = False,
        auto_recover: bool = True
    ) -> Optional[InscribedBlock]:
        """
        Safely transition block to inscribed state with validation and error handling.
        
        Args:
            block: The LiveBlock to transition
            force: Skip validation if True (dangerous)
            auto_recover: Attempt automatic recovery on failure
            
        Returns:
            InscribedBlock if successful, None if failed
            
        Raises:
            ValidationError: If validation fails and force=False
            InscriptionError: If inscription fails after all retries
        """
        async with self.transition_context(block, BlockState.INSCRIBED) as transition_state:
            
            # Validation phase (unless forced)
            if not force:
                validation_result = await self.validate_transition(block, BlockState.INSCRIBED)
                
                if not validation_result.is_valid:
                    error_msg = f"Block {block.id} failed inscription validation: {validation_result.error_messages}"
                    raise ValidationError(error_msg)
                
                # Log warnings but continue
                for warning in validation_result.warnings:
                    print(f"Warning during transition of block {block.id}: {warning}")
            
            # Attempt inscription with retries
            last_exception = None
            for attempt in range(self._max_retry_attempts):
                transition_state.attempt_count = attempt + 1
                
                try:
                    # Store rollback data
                    transition_state.rollback_data = {
                        'original_state': block.state,
                        'original_content': block.data.content,
                        'original_progress': block.data.progress
                    }
                    
                    # Perform the inscription
                    inscribed_block = await block.to_inscribed_block()
                    
                    # Success - clear transition state
                    return inscribed_block
                    
                except Exception as e:
                    last_exception = e
                    transition_state.last_error = e
                    
                    print(f"Inscription attempt {attempt + 1} failed for block {block.id}: {e}")
                    
                    # Attempt recovery if enabled and not the last attempt
                    if auto_recover and attempt < self._max_retry_attempts - 1:
                        print(f"Attempting recovery for block {block.id}")
                        
                        recovery_success = False
                        for strategy in self._recovery_strategies:
                            try:
                                if await strategy.recover(transition_state, block):
                                    recovery_success = True
                                    break
                            except Exception as recovery_error:
                                print(f"Recovery strategy failed: {recovery_error}")
                        
                        if not recovery_success:
                            print(f"All recovery strategies failed for block {block.id}")
                            break
                        
                        # Wait before retry
                        await asyncio.sleep(0.5 * (attempt + 1))
                    else:
                        break
            
            # All attempts failed
            error_msg = f"Failed to inscribe block {block.id} after {self._max_retry_attempts} attempts"
            if last_exception:
                error_msg += f". Last error: {last_exception}"
            
            raise InscriptionError(error_msg)
    
    def get_active_transitions(self) -> Dict[str, TransitionState]:
        """Get currently active transitions."""
        with self._transition_lock:
            return self._active_transitions.copy()
    
    async def cancel_transition(self, block_id: str) -> bool:
        """Cancel an active transition."""
        with self._transition_lock:
            if block_id in self._active_transitions:
                transition_state = self._active_transitions[block_id]
                # Mark as cancelled (implementation depends on specific needs)
                print(f"Cancelling transition for block {block_id}")
                return True
            return False
    
    def get_transition_statistics(self) -> Dict[str, Any]:
        """Get statistics about transitions."""
        with self._transition_lock:
            active_count = len(self._active_transitions)
            
            # Could expand with more detailed stats
            return {
                'active_transitions': active_count,
                'transition_ids': list(self._active_transitions.keys())
            }


# Global instance for application use
transition_manager = BlockTransitionManager()


# Convenience functions for common operations
async def safe_inscribe_block(
    block: LiveBlock,
    force: bool = False,
    auto_recover: bool = True
) -> Optional[InscribedBlock]:
    """Convenience function for safe block inscription."""
    return await transition_manager.transition_to_inscribed(
        block=block,
        force=force,
        auto_recover=auto_recover
    )


async def validate_block_ready_for_inscription(block: LiveBlock) -> TransitionValidationResult:
    """Convenience function for validation check."""
    return await transition_manager.validate_transition(block, BlockState.INSCRIBED)