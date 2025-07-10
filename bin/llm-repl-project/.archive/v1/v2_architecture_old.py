#!/usr/bin/env python3
"""
V2 Architecture: Clean Block Lifecycle System

Core principles:
1. Common lifecycle: Live (active) → Inscribed (immutable)
2. Clear separation of concerns
3. Model/provider agnostic design
4. Extensible for future features
5. Zero regression migration path
"""

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Union
from pathlib import Path

# Import refactored modules
from providers.base import LLMProvider, TokenCounts, LLMResponse
from providers.manager import LLMManager

# ============================================================================
# CORE TYPES AND ENUMS
# ============================================================================

class BlockState(Enum):
    """Block lifecycle states."""
    CREATED = "created"
    LIVE_WAITING = "live_waiting"  
    LIVE_PROCESSING = "live_processing"
    LIVE_STREAMING = "live_streaming"
    INSCRIBED = "inscribed"

@dataclass
class Artifact:
    """Copyable artifact (code, data, etc.)."""
    content: str
    artifact_type: str  # "code", "data", "image", etc.
    language: Optional[str] = None
    title: Optional[str] = None
    copyable: bool = True

@dataclass
class DisplayContent:
    """Content for display rendering."""
    title: str
    message: str
    tokens: Optional[TokenCounts] = None
    elapsed_time: float = 0.0
    progress: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

# ============================================================================
# CORE INTERFACES
# ============================================================================

class DisplayRenderer(Protocol):
    """Protocol for rendering block content."""
    
    def render_live_content(self, content: DisplayContent) -> None:
        """Render content in live state."""
        ...
    
    def render_inscribed_content(self, content: DisplayContent) -> None:
        """Render content in inscribed state."""
        ...

class LLMInterface(Protocol):
    """Protocol for LLM implementations."""
    
    async def make_request(self, prompt: str, options: Dict[str, Any] = None) -> LLMResponse:
        """Make a request to the LLM."""
        ...
    
    def get_provider(self) -> LLMProvider:
        """Get the LLM provider."""
        ...
    
    def get_model(self) -> str:
        """Get the model name."""
        ...

# ============================================================================
# BASE BLOCK - COMMON LIFECYCLE PATTERN
# ============================================================================

class BaseBlock(ABC):
    """
    Base class for all blocks with common live → inscribed lifecycle.
    """
    
    def __init__(self, title: str):
        self.unique_id = str(uuid.uuid4())
        self.title = title
        self.state = BlockState.CREATED
        self.created_at = time.time()
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        # Display management
        self.renderer: Optional[DisplayRenderer] = None
        self.live_content: Optional[DisplayContent] = None
        self.inscribed_content: Optional[DisplayContent] = None
    
    def transition_to_live(self, initial_state: BlockState = BlockState.LIVE_WAITING) -> None:
        """Transition from created to live state."""
        if self.state != BlockState.CREATED:
            raise ValueError(f"Can only transition to live from CREATED state, current: {self.state}")
        
        self.state = initial_state
        self.start_time = time.time()
        self._on_live_start()
    
    def update_live_state(self, new_state: BlockState) -> None:
        """Update live state (waiting → processing → streaming)."""
        if not self._is_live_state(new_state):
            raise ValueError(f"Not a valid live state: {new_state}")
        
        old_state = self.state
        self.state = new_state
        self._on_live_state_change(old_state, new_state)
    
    def transition_to_inscribed(self) -> 'InscribedBlock':
        """Transition to final inscribed state."""
        if not self._is_live_state(self.state):
            raise ValueError(f"Can only transition to inscribed from live state, current: {self.state}")
        
        self.state = BlockState.INSCRIBED
        self.end_time = time.time()
        
        # Create final inscribed content
        self.inscribed_content = self._create_inscribed_content()
        
        # Create immutable inscribed block
        inscribed = InscribedBlock(
            original_id=self.unique_id,
            title=self.title,
            content=self.inscribed_content,
            created_at=self.created_at,
            duration=self.get_duration()
        )
        
        self._on_inscribed()
        return inscribed
    
    def get_duration(self) -> float:
        """Get block duration."""
        if not self.start_time:
            return 0.0
        end = self.end_time or time.time()
        return end - self.start_time
    
    def get_current_display_content(self) -> DisplayContent:
        """Get current display content based on state."""
        if self.state == BlockState.INSCRIBED and self.inscribed_content:
            return self.inscribed_content
        return self._create_live_display_content()
    
    @staticmethod
    def _is_live_state(state: BlockState) -> bool:
        """Check if state is a live state."""
        return state in [BlockState.LIVE_WAITING, BlockState.LIVE_PROCESSING, BlockState.LIVE_STREAMING]
    
    # Abstract methods that subclasses must implement
    @abstractmethod
    def _on_live_start(self) -> None:
        """Called when transitioning to live state."""
        pass
    
    @abstractmethod
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Called when live state changes."""
        pass
    
    @abstractmethod
    def _create_live_display_content(self) -> DisplayContent:
        """Create display content for live state."""
        pass
    
    @abstractmethod
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed display content."""
        pass
    
    @abstractmethod
    def _on_inscribed(self) -> None:
        """Called when transitioning to inscribed state."""
        pass

# ============================================================================
# INSCRIBED BLOCK - IMMUTABLE FINAL FORM
# ============================================================================

@dataclass(frozen=True)
class InscribedBlock:
    """Immutable final form of a block for history and logs."""
    original_id: str
    title: str
    content: DisplayContent
    created_at: float
    duration: float
    
    def to_log_entry(self) -> Dict[str, Any]:
        """Convert to log entry format."""
        return {
            "id": self.original_id,
            "title": self.title,
            "content": self.content.message,
            "tokens": self.content.tokens.__dict__ if self.content.tokens else None,
            "duration": self.duration,
            "timestamp": self.created_at
        }

# ============================================================================
# 3. PROCESSING SUB-BLOCK - INDIVIDUAL PROCESSING STEP
# ============================================================================

class ProcessingSubBlock(BaseBlock):
    """
    Individual processing step with own clock, LLM, tokens, methodology.
    Model/provider agnostic and self-managing.
    """
    
    def __init__(self, 
                 title: str, 
                 methodology: str,
                 llm_manager: Optional[LLMManager] = None):
        super().__init__(title)
        self.methodology = methodology
        self.llm_manager = llm_manager
        
        # Processing results
        self.input_data: Any = None
        self.output_data: Any = None
        self.llm_response: Optional[LLMResponse] = None
        self.error: Optional[Exception] = None
        
        # Progress tracking
        self.progress: float = 0.0
        self.status_message: str = "Waiting to start"
    
    async def execute(self, input_data: Any) -> Any:
        """Execute this processing step."""
        self.input_data = input_data
        self.transition_to_live(BlockState.LIVE_PROCESSING)
        
        try:
            self.status_message = "Processing..."
            self.progress = 0.1
            
            # Execute the actual processing logic
            result = await self._execute_processing_logic(input_data)
            
            self.output_data = result
            self.progress = 1.0
            self.status_message = "Completed"
            
            return result
            
        except Exception as e:
            self.error = e
            self.status_message = f"Failed: {str(e)}"
            raise
    
    async def _execute_processing_logic(self, input_data: Any) -> Any:
        """Override this in subclasses for specific processing logic."""
        # Default: if we have an LLM manager, make a request
        if self.llm_manager and isinstance(input_data, str):
            self.progress = 0.3
            self.status_message = "Calling LLM..."
            
            self.llm_response = await self.llm_manager.make_request(input_data)
            
            self.progress = 0.9
            self.status_message = "Processing response..."
            
            return self.llm_response.content
        
        # Default passthrough
        return input_data
    
    def _on_live_start(self) -> None:
        """Called when starting live state."""
        self.status_message = "Starting..."
    
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Called when live state changes."""
        if new_state == BlockState.LIVE_PROCESSING:
            self.status_message = "Processing..."
    
    def _create_live_display_content(self) -> DisplayContent:
        """Create live display content."""
        tokens = self.llm_response.tokens if self.llm_response else None
        
        return DisplayContent(
            title=self.title,
            message=f"{self.status_message} ({self.get_duration():.1f}s)",
            tokens=tokens,
            elapsed_time=self.get_duration(),
            progress=self.progress,
            metadata={
                "methodology": self.methodology,
                "state": self.state.value
            }
        )
    
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed content."""
        tokens = self.llm_response.tokens if self.llm_response else None
        
        status = "Completed" if not self.error else f"Failed: {self.error}"
        
        return DisplayContent(
            title=self.title,
            message=f"{status} ({self.get_duration():.1f}s)",
            tokens=tokens,
            elapsed_time=self.get_duration(),
            progress=1.0 if not self.error else 0.0,
            metadata={
                "methodology": self.methodology,
                "final_state": "completed" if not self.error else "failed"
            }
        )
    
    def _on_inscribed(self) -> None:
        """Called when transitioning to inscribed."""
        pass

# ============================================================================
# 4. INTERNAL PROCESSING BLOCK - PIPELINE MANAGER
# ============================================================================

class InternalProcessingBlock(BaseBlock):
    """
    Manages sequential list of sub-processes and their display.
    Coordinates the entire processing pipeline.
    """
    
    def __init__(self, title: str = "Internal Processing", scrivener=None):
        super().__init__(title)
        self.sub_blocks: List[ProcessingSubBlock] = []
        self.current_sub_block_index: int = 0
        self.pipeline_input: Any = None
        self.pipeline_output: Any = None
        self.scrivener = scrivener
        
        # Display management
        self.display_layout: str = "vertical"  # "vertical" or "horizontal"
        
    def add_sub_block(self, sub_block: ProcessingSubBlock) -> None:
        """Add a sub-processing block to the pipeline."""
        self.sub_blocks.append(sub_block)
    
    async def execute_pipeline(self, input_data: Any) -> Any:
        """Execute all sub-blocks in sequence."""
        self.pipeline_input = input_data
        self.transition_to_live(BlockState.LIVE_PROCESSING)
        
        try:
            current_data = input_data
            
            for i, sub_block in enumerate(self.sub_blocks):
                self.current_sub_block_index = i
                
                # Execute sub-block
                current_data = await sub_block.execute(current_data)
                
                # Update our display
                await self._update_pipeline_display()
            
            self.pipeline_output = current_data
            return current_data
            
        except Exception as e:
            # Handle pipeline failure
            raise
    
    def get_total_tokens(self) -> TokenCounts:
        """Get total tokens used across all sub-blocks."""
        total = TokenCounts()
        for sub_block in self.sub_blocks:
            if sub_block.llm_response:
                total.input_tokens += sub_block.llm_response.tokens.input_tokens
                total.output_tokens += sub_block.llm_response.tokens.output_tokens
        return total
    
    async def _update_pipeline_display(self) -> None:
        """Update pipeline display based on current state."""
        if self.scrivener:
            # Send processing update event to scrivener
            current_block = self.sub_blocks[self.current_sub_block_index]
            
            # Try to import the scrivener types
            try:
                from scrivener import InscriptionEvent, EventType
                
                # Create processing update event
                event = InscriptionEvent(
                    event_type=EventType.PROCESSING_UPDATE,
                    content=f"Processing: {current_block.title}",
                    metadata={
                        "step": self.current_sub_block_index + 1,
                        "total": len(self.sub_blocks),
                        "methodology": current_block.methodology
                    }
                )
                
                # Inscribe the event
                await self.scrivener.inscribe(event)
                    
            except ImportError:
                # If scrivener is not available, skip
                pass
    
    def _on_live_start(self) -> None:
        """Called when starting live state."""
        pass
    
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Called when live state changes."""
        pass
    
    def _create_live_display_content(self) -> DisplayContent:
        """Create live display content showing pipeline progress."""
        total_tokens = self.get_total_tokens()
        
        # Create progress message
        if self.current_sub_block_index < len(self.sub_blocks):
            current_block = self.sub_blocks[self.current_sub_block_index]
            progress_msg = f"Step {self.current_sub_block_index + 1}/{len(self.sub_blocks)}: {current_block.title}"
        else:
            progress_msg = f"Completed all {len(self.sub_blocks)} steps"
        
        return DisplayContent(
            title=self.title,
            message=progress_msg,
            tokens=total_tokens,
            elapsed_time=self.get_duration(),
            progress=self.current_sub_block_index / len(self.sub_blocks) if self.sub_blocks else 1.0,
            metadata={
                "sub_blocks": len(self.sub_blocks),
                "current_step": self.current_sub_block_index + 1
            }
        )
    
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed content."""
        total_tokens = self.get_total_tokens()
        
        return DisplayContent(
            title=self.title,
            message=f"Completed {len(self.sub_blocks)} processing steps ({self.get_duration():.1f}s total)",
            tokens=total_tokens,
            elapsed_time=self.get_duration(),
            progress=1.0,
            metadata={
                "sub_blocks": len(self.sub_blocks),
                "final_state": "completed"
            }
        )
    
    def _on_inscribed(self) -> None:
        """Called when transitioning to inscribed."""
        # Ensure all sub-blocks are also inscribed
        for sub_block in self.sub_blocks:
            if sub_block.state != BlockState.INSCRIBED:
                sub_block.transition_to_inscribed()
    
    def finalize_for_history(self) -> Dict[str, Any]:
        """Create final form for history log."""
        # Transition to inscribed if not already
        if self.state != BlockState.INSCRIBED:
            inscribed = self.transition_to_inscribed()
        else:
            inscribed = InscribedBlock(
                original_id=self.unique_id,
                title=self.title,
                content=self.inscribed_content or self._create_inscribed_content(),
                created_at=self.created_at,
                duration=self.get_duration()
            )
        
        # Handle sub-blocks
        sub_block_entries = []
        for sub in self.sub_blocks:
            if sub.state != BlockState.INSCRIBED:
                sub_inscribed = sub.transition_to_inscribed()
            else:
                sub_inscribed = InscribedBlock(
                    original_id=sub.unique_id,
                    title=sub.title,
                    content=sub.inscribed_content or sub._create_inscribed_content(),
                    created_at=sub.created_at,
                    duration=sub.get_duration()
                )
            sub_block_entries.append(sub_inscribed.to_log_entry())
        
        return {
            "pipeline_summary": inscribed.to_log_entry(),
            "sub_blocks": sub_block_entries,
            "total_tokens": self.get_total_tokens().__dict__,
            "total_duration": self.get_duration()
        }

# ============================================================================
# 5. RESEARCH ASSISTANT RESPONSE - EXTENSIBLE RESPONSE MANAGEMENT
# ============================================================================

@dataclass
class ToolResult:
    """Result from a tool call."""
    tool_name: str
    input_data: Any
    output_data: Any
    success: bool
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class ResearchAssistantResponse(BaseBlock):
    """
    Manages research assistant responses with extensibility for 
    tool calls, artifacts, images, and complex rendering.
    """
    
    def __init__(self, content: str, routing_metadata: Dict[str, Any] = None):
        super().__init__("Research Assistant Response")
        self.content = content
        self.routing_metadata = routing_metadata or {}
        
        # Extensible components
        self.artifacts: List[Artifact] = []
        self.tool_results: List[ToolResult] = []
        self.images: List[str] = []  # Image paths/URLs
        self.rendered_content: Optional[str] = None
        
        # Processing state
        self.is_streaming: bool = False
        self.stream_position: int = 0
    
    def add_artifact(self, artifact: Artifact) -> None:
        """Add a copyable artifact (code, data, etc.)."""
        self.artifacts.append(artifact)
    
    def add_tool_result(self, tool_result: ToolResult) -> None:
        """Add a tool execution result."""
        self.tool_results.append(tool_result)
    
    def add_image(self, image_path: str) -> None:
        """Add an image for terminal display."""
        self.images.append(image_path)
    
    def start_streaming(self) -> None:
        """Start streaming response content."""
        self.is_streaming = True
        self.stream_position = 0
        self.transition_to_live(BlockState.LIVE_STREAMING)
    
    def update_stream(self, new_content: str) -> None:
        """Update streaming content."""
        if self.is_streaming:
            self.content = new_content
            self.stream_position = len(new_content)
    
    def complete_streaming(self) -> None:
        """Complete streaming response."""
        self.is_streaming = False
        self.update_live_state(BlockState.LIVE_PROCESSING)
    
    def extract_code_artifacts(self) -> List[Artifact]:
        """Extract code blocks as artifacts."""
        import re
        
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', self.content, re.DOTALL)
        artifacts = []
        
        for lang, code in code_blocks:
            artifact = Artifact(
                content=code.strip(),
                artifact_type="code",
                language=lang or "text",
                title=f"Code snippet ({lang or 'text'})",
                copyable=True
            )
            artifacts.append(artifact)
            
        return artifacts
    
    def render_for_terminal(self) -> str:
        """Render content for terminal display with tool results, images, etc."""
        if self.rendered_content:
            return self.rendered_content
        
        # Start with base content
        rendered = self.content
        
        # Add tool results
        if self.tool_results:
            rendered += "\n\n--- Tool Results ---\n"
            for tool_result in self.tool_results:
                status = "✅" if tool_result.success else "❌"
                rendered += f"{status} {tool_result.tool_name}: {tool_result.output_data}\n"
        
        # Add artifact summaries
        if self.artifacts:
            rendered += "\n\n--- Artifacts ---\n"
            for artifact in self.artifacts:
                rendered += f"📄 {artifact.title} ({artifact.artifact_type})\n"
        
        # Add image indicators
        if self.images:
            rendered += "\n\n--- Images ---\n"
            for image in self.images:
                rendered += f"🖼️  {image}\n"
        
        self.rendered_content = rendered
        return rendered
    
    def _on_live_start(self) -> None:
        """Called when starting live state."""
        # Auto-extract code artifacts
        self.artifacts.extend(self.extract_code_artifacts())
    
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Called when live state changes."""
        if new_state == BlockState.LIVE_STREAMING:
            self.start_streaming()
    
    def _create_live_display_content(self) -> DisplayContent:
        """Create live display content."""
        if self.is_streaming:
            message = f"Streaming response... ({self.stream_position} chars)"
        else:
            message = self.render_for_terminal()
        
        return DisplayContent(
            title=self.title,
            message=message,
            tokens=None,  # Response doesn't track tokens directly
            elapsed_time=self.get_duration(),
            progress=1.0 if not self.is_streaming else 0.5,
            metadata={
                "artifacts": len(self.artifacts),
                "tool_results": len(self.tool_results),
                "images": len(self.images),
                "routing": self.routing_metadata
            }
        )
    
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed content."""
        return DisplayContent(
            title=self.title,
            message=self.render_for_terminal(),
            tokens=None,
            elapsed_time=self.get_duration(),
            progress=1.0,
            metadata={
                "artifacts": len(self.artifacts),
                "tool_results": len(self.tool_results),
                "images": len(self.images),
                "routing": self.routing_metadata,
                "final_state": "completed"
            }
        )
    
    def _on_inscribed(self) -> None:
        """Called when transitioning to inscribed."""
        # Ensure rendered content is finalized
        self.render_for_terminal()

# ============================================================================
# 6. USER INPUT BLOCK - EXTENSIBLE INPUT MANAGEMENT
# ============================================================================

@dataclass
class ShellCommand:
    """Embedded shell command."""
    command: str
    args: List[str]
    output: Optional[str] = None
    success: bool = True

@dataclass
class Attachment:
    """File attachment (image, document, etc.)."""
    path: str
    attachment_type: str  # "image", "document", "audio", etc.
    size_bytes: int
    metadata: Dict[str, Any] = field(default_factory=dict)

class UserInputBlock(BaseBlock):
    """
    Manages user input with extensibility for complex inputs:
    - Multi-line text
    - Image attachments
    - Embedded shell commands
    - File uploads
    """
    
    def __init__(self):
        super().__init__("User Input")
        self.text_content: str = ""
        self.attachments: List[Attachment] = []
        self.shell_commands: List[ShellCommand] = []
        self.is_multiline: bool = False
        
        # Input state
        self.input_complete: bool = False
        self.cursor_position: int = 0
    
    async def collect_input(self) -> Dict[str, Any]:
        """Collect user input with support for complex inputs."""
        self.transition_to_live(BlockState.LIVE_WAITING)
        
        try:
            # Basic text input (placeholder for real implementation)
            self.text_content = await self._collect_text_input()
            
            # Parse embedded commands
            self.shell_commands = self._parse_embedded_commands(self.text_content)
            
            # Check for clipboard images
            await self._check_clipboard_attachments()
            
            # Mark as complete
            self.input_complete = True
            self.update_live_state(BlockState.LIVE_PROCESSING)
            
            return {
                "text": self.text_content,
                "attachments": self.attachments,
                "shell_commands": self.shell_commands
            }
            
        except Exception as e:
            raise
    
    async def _collect_text_input(self) -> str:
        """Collect text input (placeholder for real implementation)."""
        # In real implementation, this would use prompt_toolkit or similar
        return input("Enter your input: ")
    
    def _parse_embedded_commands(self, text: str) -> List[ShellCommand]:
        """Parse embedded shell commands from text."""
        import re
        
        # Look for commands like: $(ls -la) or `git status`
        command_pattern = r'`([^`]+)`|\$\(([^)]+)\)'
        commands = []
        
        for match in re.finditer(command_pattern, text):
            cmd_text = match.group(1) or match.group(2)
            parts = cmd_text.split()
            if parts:
                command = ShellCommand(
                    command=parts[0],
                    args=parts[1:] if len(parts) > 1 else []
                )
                commands.append(command)
        
        return commands
    
    async def _check_clipboard_attachments(self) -> None:
        """Check clipboard for image attachments."""
        # Placeholder for clipboard image detection
        # In real implementation, would check system clipboard
        pass
    
    def add_attachment(self, attachment: Attachment) -> None:
        """Add a file attachment."""
        self.attachments.append(attachment)
    
    def execute_shell_commands(self) -> None:
        """Execute embedded shell commands."""
        import subprocess
        
        for cmd in self.shell_commands:
            try:
                result = subprocess.run(
                    [cmd.command] + cmd.args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                cmd.output = result.stdout
                cmd.success = result.returncode == 0
            except Exception as e:
                cmd.output = f"Error: {str(e)}"
                cmd.success = False
    
    def _on_live_start(self) -> None:
        """Called when starting live state."""
        pass
    
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Called when live state changes."""
        if new_state == BlockState.LIVE_PROCESSING:
            # Execute any shell commands
            self.execute_shell_commands()
    
    def _create_live_display_content(self) -> DisplayContent:
        """Create live display content."""
        if not self.input_complete:
            message = "Waiting for input..."
        else:
            message = f"Input: {self.text_content}"
            if self.attachments:
                message += f" ({len(self.attachments)} attachments)"
            if self.shell_commands:
                message += f" ({len(self.shell_commands)} commands)"
        
        return DisplayContent(
            title=self.title,
            message=message,
            tokens=None,
            elapsed_time=self.get_duration(),
            progress=1.0 if self.input_complete else 0.0,
            metadata={
                "text_length": len(self.text_content),
                "attachments": len(self.attachments),
                "shell_commands": len(self.shell_commands),
                "multiline": self.is_multiline
            }
        )
    
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed content."""
        return DisplayContent(
            title=self.title,
            message=self.text_content,
            tokens=None,
            elapsed_time=self.get_duration(),
            progress=1.0,
            metadata={
                "text_length": len(self.text_content),
                "attachments": len(self.attachments),
                "shell_commands": len(self.shell_commands),
                "final_state": "completed"
            }
        )
    
    def _on_inscribed(self) -> None:
        """Called when transitioning to inscribed."""
        pass

# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

if __name__ == "__main__":
    # Example usage of the new architecture
    
    async def demo_v2_architecture():
        """Demonstrate the complete V2 architecture."""
        print("🏗️  V2 Architecture Complete Demo")
        print("=" * 60)
        
        # 1. Create LLM Manager (source of truth for tokens)
        llm_manager = LLMManager(LLMProvider.OLLAMA, "tinyllama")
        print("✅ LLM Manager created")
        
        # 2. Create User Input Block
        user_input = UserInputBlock()
        print("✅ User Input Block created")
        
        # 3. Create Processing Pipeline
        pipeline = InternalProcessingBlock("Query Processing Pipeline")
        
        # Add intent detection sub-block
        intent_block = ProcessingSubBlock(
            title="Intent Detection",
            methodology="TinyLlama Classification", 
            llm_manager=llm_manager
        )
        pipeline.add_sub_block(intent_block)
        
        # Add query processing sub-block
        query_block = ProcessingSubBlock(
            title="Query Processing",
            methodology="TinyLlama Generation",
            llm_manager=llm_manager
        )
        pipeline.add_sub_block(query_block)
        
        print("✅ Processing pipeline created with 2 sub-blocks")
        
        # 4. Execute complete pipeline
        print("\n🚀 Starting complete pipeline execution...")
        
        query = "What is machine learning?"
        
        # Execute pipeline
        result = await pipeline.execute_pipeline(query)
        print(f"✅ Pipeline completed: {result[:50]}...")
        
        # 5. Create Research Assistant Response
        response = ResearchAssistantResponse(
            content=result,
            routing_metadata={"intent": "CHAT", "method": "AI_CLASSIFIED"}
        )
        
        # Add some artifacts (simulated)
        response.add_artifact(Artifact(
            content="def machine_learning():\n    return 'AI algorithm'",
            artifact_type="code",
            language="python",
            title="ML Function Example"
        ))
        
        response.transition_to_live()
        print("✅ Research Assistant Response created with artifacts")
        
        # 6. Show comprehensive results
        print("\n📊 COMPREHENSIVE RESULTS")
        print("=" * 60)
        
        # LLM Manager summary
        summary = llm_manager.get_session_summary()
        print(f"🧠 LLM Summary: {summary['total_requests']} requests, {summary['total_tokens']} tokens")
        
        # Pipeline summary
        pipeline_history = pipeline.finalize_for_history()
        print(f"⚙️  Pipeline: {len(pipeline_history['sub_blocks'])} steps, {pipeline_history['total_duration']:.1f}s")
        
        # Response summary
        response_inscribed = response.transition_to_inscribed()
        print(f"📝 Response: {len(response.artifacts)} artifacts, {len(response.tool_results)} tool results")
        
        # Token breakdown
        print("\n🔢 TOKEN BREAKDOWN")
        print("-" * 30)
        for i, sub_block in enumerate(pipeline.sub_blocks):
            if sub_block.llm_response:
                tokens = sub_block.llm_response.tokens
                print(f"Step {i+1} ({sub_block.title}): ↑{tokens.input_tokens} ↓{tokens.output_tokens}")
        
        total_tokens = pipeline.get_total_tokens()
        print(f"Total: ↑{total_tokens.input_tokens} ↓{total_tokens.output_tokens}")
        
        print("\n✨ V2 Architecture Demo Complete!")
        print("🎯 Key Features Demonstrated:")
        print("  - Central LLM token management")
        print("  - Live → Inscribed block lifecycle")
        print("  - Pipeline coordination")
        print("  - Extensible response management")
        print("  - Clean separation of concerns")
    
    # Run demo
    asyncio.run(demo_v2_architecture())