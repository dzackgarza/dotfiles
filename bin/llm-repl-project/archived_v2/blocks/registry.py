"""Block registry and sequence validation."""

from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Field, field_validator, ConfigDict
from .base import Block, BlockType


class BlockSequenceRule(BaseModel):
    """Defines valid block sequences."""
    query_type: str = "default"
    expected_sequence: List[BlockType] = Field(
        default_factory=lambda: [
            BlockType.SYSTEM_CHECK,
            BlockType.WELCOME,
            BlockType.USER,
            BlockType.INTERNAL_PROCESSING,
            BlockType.ASSISTANT
        ]
    )
    
    @field_validator('expected_sequence')
    def validate_sequence(cls, v):
        if not v:
            raise ValueError("Sequence cannot be empty")
        return v


class BlockSequence(BaseModel):
    """
    Represents an ordered sequence of blocks.
    This is the source of truth for what was displayed to the user.
    """
    blocks: List[Block] = Field(default_factory=list)
    sequence_rules: Dict[str, BlockSequenceRule] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add default sequence rule
        self.sequence_rules["default"] = BlockSequenceRule()
    
    def add_block(self, block: Block) -> None:
        """Add a block to the sequence."""
        self.blocks.append(block)
    
    def get_block_types(self) -> List[BlockType]:
        """Get the sequence of block types."""
        return [block.metadata.type for block in self.blocks]
    
    def validate_sequence(self, query_type: str = "default") -> bool:
        """
        Validate that the block sequence matches expected patterns.
        This is our primary regression test.
        """
        rule = self.sequence_rules.get(query_type, self.sequence_rules["default"])
        actual_types = self.get_block_types()
        expected_types = rule.expected_sequence
        
        # For now, check that all expected types are present in order
        # (allowing for additional blocks between them)
        expected_idx = 0
        for actual_type in actual_types:
            if expected_idx < len(expected_types) and actual_type == expected_types[expected_idx]:
                expected_idx += 1
        
        return expected_idx == len(expected_types)
    
    def get_validation_report(self, query_type: str = "default") -> Dict[str, any]:
        """Get a detailed validation report."""
        rule = self.sequence_rules.get(query_type, self.sequence_rules["default"])
        actual_types = self.get_block_types()
        expected_types = rule.expected_sequence
        
        # Find missing and extra blocks
        missing = []
        extra = []
        matched = []
        
        expected_set = set(expected_types)
        actual_set = set(actual_types)
        
        for block_type in expected_types:
            if block_type not in actual_set:
                missing.append(block_type)
            else:
                matched.append(block_type)
        
        for block_type in actual_types:
            if block_type not in expected_set:
                extra.append(block_type)
        
        return {
            "valid": self.validate_sequence(query_type),
            "expected": expected_types,
            "actual": actual_types,
            "missing": missing,
            "extra": extra,
            "matched": matched,
            "query_type": query_type
        }
    
    def to_display_list(self) -> List[Dict[str, any]]:
        """Convert blocks to display format."""
        return [block.render() for block in self.blocks]
    
    def to_history(self) -> List[Dict[str, any]]:
        """Convert blocks to historical record format."""
        return [block.to_dict() for block in self.blocks]


class BlockRegistry:
    """
    Central registry for all blocks in the system.
    Maintains the authoritative record of what was displayed.
    """
    
    def __init__(self):
        self.sequences: List[BlockSequence] = []
        self.current_sequence: Optional[BlockSequence] = None
        self.all_blocks: Dict[str, Block] = {}
    
    def start_new_sequence(self) -> BlockSequence:
        """Start a new block sequence."""
        self.current_sequence = BlockSequence()
        self.sequences.append(self.current_sequence)
        return self.current_sequence
    
    def register_block(self, block: Block) -> None:
        """Register a block in the system."""
        self.all_blocks[block.id] = block
        if self.current_sequence:
            self.current_sequence.add_block(block)
    
    def get_block(self, block_id: str) -> Optional[Block]:
        """Get a block by ID."""
        return self.all_blocks.get(block_id)
    
    def get_current_sequence(self) -> Optional[BlockSequence]:
        """Get the current block sequence."""
        return self.current_sequence
    
    def validate_current_sequence(self, query_type: str = "default") -> bool:
        """Validate the current sequence."""
        if not self.current_sequence:
            return False
        return self.current_sequence.validate_sequence(query_type)
    
    def get_validation_report(self, query_type: str = "default") -> Dict[str, any]:
        """Get validation report for current sequence."""
        if not self.current_sequence:
            return {
                "valid": False,
                "error": "No current sequence"
            }
        return self.current_sequence.get_validation_report(query_type)