# Context Deduplication System

**Branch:** feat/context-deduplication-system
**Summary:** Implement intelligent context deduplication to avoid storing redundant file contents, git states, and system information in every timeline block, directly solving the Cursor agent massive context storage problem.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
Based on Cursor agent analysis, the database bloats because **each chat message stores full context** (file contents, git status, terminal state, editor state) leading to 200KB+ per message. This treats SQLite as an "infinite append-only log" which causes 500+ MB databases. We need **intelligent context deduplication** that stores context efficiently while maintaining full contextual access.

### Cursor Agent Problems Identified
- **Message contexts**: ~288KB each (full file contents included)
- **File system snapshots**: Complete file trees stored repeatedly
- **Git status history**: Redundant git state in every message
- **Terminal/Editor state**: Full state dumps accumulating over time
- **No deduplication**: Identical contexts stored multiple times

### Success Criteria
- [ ] Context storage reduced by 90%+ through intelligent deduplication
- [ ] Full context reconstructable for any historical conversation
- [ ] Context changes tracked efficiently through diffs
- [ ] Reference integrity maintained across timeline
- [ ] Performance improved through reduced storage overhead

### Acceptance Criteria
- [ ] Timeline blocks store context references, not full context
- [ ] Identical file contents stored only once with content hashing
- [ ] Git states use incremental diffs instead of full snapshots
- [ ] Context reconstruction is transparent to plugins and UI
- [ ] Database size grows linearly with unique content, not conversation length

## Technical Approach

### Architecture Changes
1. **Context Store**: Centralized storage for unique contexts with content hashing
2. **Reference System**: Timeline blocks store lightweight context references
3. **Diff Engine**: Track context changes efficiently through incremental diffs
4. **Reconstruction Engine**: Rebuild full context from references on demand
5. **Cleanup System**: Garbage collection for unreferenced contexts

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

### Dependencies
- Sacred Timeline Persistence (foundation for context storage)
- Intelligent Timeline Archival (works with archival system)
- Plugin Architecture Foundation (context access for plugins)

### Risks & Mitigations
- **Risk 1**: Context reconstruction performance overhead
  - *Mitigation*: Aggressive caching, lazy loading, background reconstruction
- **Risk 2**: Complex reference management leading to broken contexts
  - *Mitigation*: Strong referential integrity, validation, rollback mechanisms
- **Risk 3**: Diff computation complexity for large contexts
  - *Mitigation*: Efficient diff algorithms, chunking, parallel processing

## Context Deduplication Architecture

### Content Hashing System
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Set
import hashlib
import json
import gzip
from datetime import datetime

@dataclass
class ContextHash:
    """Unique identifier for context content."""
    algorithm: str = "sha256"
    digest: str = ""
    size: int = 0
    compression_ratio: float = 1.0
    
    @classmethod
    def from_content(cls, content: Any) -> 'ContextHash':
        """Generate hash from content."""
        # Normalize content for consistent hashing
        normalized = cls._normalize_content(content)
        content_bytes = json.dumps(normalized, sort_keys=True, separators=(',', ':')).encode('utf-8')
        
        # Compress for storage efficiency testing
        compressed = gzip.compress(content_bytes)
        compression_ratio = len(compressed) / len(content_bytes)
        
        # Generate hash
        digest = hashlib.sha256(content_bytes).hexdigest()
        
        return cls(
            algorithm="sha256",
            digest=digest,
            size=len(content_bytes),
            compression_ratio=compression_ratio
        )
    
    @staticmethod
    def _normalize_content(content: Any) -> Any:
        """Normalize content for consistent hashing."""
        if isinstance(content, dict):
            # Remove timestamps and transient data
            normalized = {}
            for key, value in content.items():
                if key not in ['timestamp', 'last_accessed', 'temp_data']:
                    normalized[key] = ContextHash._normalize_content(value)
            return normalized
        elif isinstance(content, list):
            return [ContextHash._normalize_content(item) for item in content]
        else:
            return content

@dataclass
class ContextEntry:
    """Stored context with metadata."""
    hash: ContextHash
    content: Any
    created_at: datetime
    last_accessed: datetime
    reference_count: int = 0
    compressed: bool = False
    
    def access(self) -> None:
        """Mark context as accessed."""
        self.last_accessed = datetime.now()

class ContextStore:
    """Centralized storage for deduplicated contexts."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache: Dict[str, ContextEntry] = {}
        self._init_storage()
    
    def _init_storage(self) -> None:
        """Initialize context storage tables."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS context_entries (
                hash TEXT PRIMARY KEY,
                content BLOB NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_accessed TIMESTAMP NOT NULL,
                reference_count INTEGER DEFAULT 0,
                compressed BOOLEAN DEFAULT FALSE,
                size_bytes INTEGER NOT NULL,
                content_type TEXT NOT NULL
            )
        """)
        
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_context_last_accessed 
            ON context_entries(last_accessed)
        """)
        
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_context_ref_count 
            ON context_entries(reference_count)
        """)
    
    async def store_context(self, content: Any, content_type: str) -> ContextHash:
        """Store context and return hash reference."""
        context_hash = ContextHash.from_content(content)
        
        # Check if already stored
        if context_hash.digest in self.cache:
            entry = self.cache[context_hash.digest]
            entry.access()
            return context_hash
        
        # Check database
        existing = await self._get_from_db(context_hash.digest)
        if existing:
            self.cache[context_hash.digest] = existing
            existing.access()
            return context_hash
        
        # Store new context
        entry = ContextEntry(
            hash=context_hash,
            content=content,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            content_type=content_type
        )
        
        await self._store_to_db(entry)
        self.cache[context_hash.digest] = entry
        
        return context_hash
    
    async def get_context(self, context_hash: ContextHash) -> Optional[Any]:
        """Retrieve context by hash."""
        # Check cache first
        if context_hash.digest in self.cache:
            entry = self.cache[context_hash.digest]
            entry.access()
            return entry.content
        
        # Load from database
        entry = await self._get_from_db(context_hash.digest)
        if entry:
            self.cache[context_hash.digest] = entry
            entry.access()
            return entry.content
        
        return None
    
    async def _store_to_db(self, entry: ContextEntry) -> None:
        """Store context entry to database."""
        # Serialize and optionally compress content
        content_bytes = json.dumps(entry.content, separators=(',', ':')).encode('utf-8')
        
        if entry.hash.compression_ratio < 0.8:  # Compress if beneficial
            content_bytes = gzip.compress(content_bytes)
            entry.compressed = True
        
        await self.db.execute("""
            INSERT INTO context_entries 
            (hash, content, created_at, last_accessed, compressed, size_bytes, content_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.hash.digest,
            content_bytes,
            entry.created_at,
            entry.last_accessed,
            entry.compressed,
            len(content_bytes),
            entry.content_type
        ))
```

### Context Reference System
```python
@dataclass
class ContextReference:
    """Lightweight reference to stored context."""
    context_hash: str
    content_type: str
    snapshot_time: datetime
    diff_from: Optional[str] = None  # Hash of previous context for diffs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "context_hash": self.context_hash,
            "content_type": self.content_type,
            "snapshot_time": self.snapshot_time.isoformat(),
            "diff_from": self.diff_from
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextReference':
        return cls(
            context_hash=data["context_hash"],
            content_type=data["content_type"],
            snapshot_time=datetime.fromisoformat(data["snapshot_time"]),
            diff_from=data.get("diff_from")
        )

@dataclass 
class TimelineBlockContext:
    """Context references for a timeline block."""
    
    # File system context
    file_system: Optional[ContextReference] = None
    
    # Git repository state
    git_status: Optional[ContextReference] = None
    
    # Editor state (open files, cursor positions, etc.)
    editor_state: Optional[ContextReference] = None
    
    # Terminal state (history, working directory, etc.)
    terminal_state: Optional[ContextReference] = None
    
    # Project configuration
    project_config: Optional[ContextReference] = None
    
    # LLM conversation context
    conversation_context: Optional[ContextReference] = None

class ContextManager:
    """Manages context storage and retrieval for timeline blocks."""
    
    def __init__(self, context_store: ContextStore):
        self.context_store = context_store
        self.diff_engine = ContextDiffEngine()
    
    async def capture_current_context(self, 
                                    previous_context: Optional[TimelineBlockContext] = None) -> TimelineBlockContext:
        """Capture current system context with deduplication."""
        
        # Capture raw context data
        file_system_data = await self._capture_file_system()
        git_data = await self._capture_git_status()
        editor_data = await self._capture_editor_state()
        terminal_data = await self._capture_terminal_state()
        project_data = await self._capture_project_config()
        
        # Store contexts with deduplication
        context_refs = TimelineBlockContext()
        
        # File system context
        if file_system_data:
            fs_hash = await self.context_store.store_context(file_system_data, "file_system")
            context_refs.file_system = ContextReference(
                context_hash=fs_hash.digest,
                content_type="file_system",
                snapshot_time=datetime.now(),
                diff_from=previous_context.file_system.context_hash if previous_context and previous_context.file_system else None
            )
        
        # Git status context  
        if git_data:
            git_hash = await self.context_store.store_context(git_data, "git_status")
            context_refs.git_status = ContextReference(
                context_hash=git_hash.digest,
                content_type="git_status", 
                snapshot_time=datetime.now(),
                diff_from=previous_context.git_status.context_hash if previous_context and previous_context.git_status else None
            )
        
        # Continue for other context types...
        
        return context_refs
    
    async def reconstruct_context(self, context_refs: TimelineBlockContext) -> Dict[str, Any]:
        """Reconstruct full context from references."""
        reconstructed = {}
        
        if context_refs.file_system:
            fs_context = await self.context_store.get_context(
                ContextHash(digest=context_refs.file_system.context_hash)
            )
            reconstructed["file_system"] = fs_context
        
        if context_refs.git_status:
            git_context = await self.context_store.get_context(
                ContextHash(digest=context_refs.git_status.context_hash)
            )
            reconstructed["git_status"] = git_context
        
        # Continue for other context types...
        
        return reconstructed
    
    async def _capture_file_system(self) -> Dict[str, Any]:
        """Capture current file system state efficiently."""
        # Only capture relevant files, not entire file system
        relevant_files = await self._get_relevant_files()
        
        file_data = {}
        for file_path in relevant_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_data[file_path] = {
                    "content": content,
                    "size": len(content),
                    "modified": os.path.getmtime(file_path)
                }
            except (IOError, UnicodeDecodeError):
                # Handle binary files or access errors
                file_data[file_path] = {
                    "binary": True,
                    "size": os.path.getsize(file_path),
                    "modified": os.path.getmtime(file_path)
                }
        
        return {
            "files": file_data,
            "working_directory": os.getcwd(),
            "timestamp": datetime.now().isoformat()
        }
```

### Diff Engine for Incremental Context
```python
class ContextDiffEngine:
    """Computes and applies diffs between contexts."""
    
    def compute_diff(self, old_context: Any, new_context: Any) -> Dict[str, Any]:
        """Compute diff between two contexts."""
        if isinstance(old_context, dict) and isinstance(new_context, dict):
            return self._compute_dict_diff(old_context, new_context)
        elif isinstance(old_context, list) and isinstance(new_context, list):
            return self._compute_list_diff(old_context, new_context)
        else:
            # Simple replacement
            return {"type": "replace", "value": new_context}
    
    def _compute_dict_diff(self, old_dict: Dict, new_dict: Dict) -> Dict[str, Any]:
        """Compute diff between dictionaries."""
        diff = {
            "type": "dict_diff",
            "added": {},
            "removed": [],
            "modified": {}
        }
        
        old_keys = set(old_dict.keys())
        new_keys = set(new_dict.keys())
        
        # Added keys
        for key in new_keys - old_keys:
            diff["added"][key] = new_dict[key]
        
        # Removed keys
        diff["removed"] = list(old_keys - new_keys)
        
        # Modified keys
        for key in old_keys & new_keys:
            if old_dict[key] != new_dict[key]:
                diff["modified"][key] = self.compute_diff(old_dict[key], new_dict[key])
        
        return diff
    
    def apply_diff(self, base_context: Any, diff: Dict[str, Any]) -> Any:
        """Apply diff to base context to get new context."""
        if diff["type"] == "replace":
            return diff["value"]
        elif diff["type"] == "dict_diff":
            return self._apply_dict_diff(base_context, diff)
        elif diff["type"] == "list_diff":
            return self._apply_list_diff(base_context, diff)
        else:
            raise ValueError(f"Unknown diff type: {diff['type']}")
    
    def _apply_dict_diff(self, base_dict: Dict, diff: Dict[str, Any]) -> Dict:
        """Apply dictionary diff to base dictionary."""
        result = base_dict.copy()
        
        # Add new keys
        result.update(diff["added"])
        
        # Remove keys
        for key in diff["removed"]:
            result.pop(key, None)
        
        # Apply modifications
        for key, sub_diff in diff["modified"].items():
            if key in result:
                result[key] = self.apply_diff(result[key], sub_diff)
        
        return result
```

### Timeline Integration
```python
class DeduplicatedTimelineBlock(TimelineBlock):
    """Timeline block that uses context references instead of full context."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_refs: Optional[TimelineBlockContext] = None
        self._reconstructed_context: Optional[Dict[str, Any]] = None
    
    async def get_full_context(self, context_manager: ContextManager) -> Dict[str, Any]:
        """Get full reconstructed context on demand."""
        if self._reconstructed_context is None and self.context_refs:
            self._reconstructed_context = await context_manager.reconstruct_context(self.context_refs)
        return self._reconstructed_context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize block with context references."""
        data = super().to_dict()
        if self.context_refs:
            data["context_refs"] = {
                "file_system": self.context_refs.file_system.to_dict() if self.context_refs.file_system else None,
                "git_status": self.context_refs.git_status.to_dict() if self.context_refs.git_status else None,
                "editor_state": self.context_refs.editor_state.to_dict() if self.context_refs.editor_state else None,
                "terminal_state": self.context_refs.terminal_state.to_dict() if self.context_refs.terminal_state else None,
                "project_config": self.context_refs.project_config.to_dict() if self.context_refs.project_config else None,
            }
        return data

class ContextAwareTimeline(SacredTimeline):
    """Timeline that automatically captures and deduplicates context."""
    
    def __init__(self, context_manager: ContextManager):
        super().__init__()
        self.context_manager = context_manager
        self.last_context: Optional[TimelineBlockContext] = None
    
    async def add_block_with_context(self, **kwargs) -> str:
        """Add block with automatic context capture and deduplication."""
        
        # Capture current context
        current_context = await self.context_manager.capture_current_context(self.last_context)
        
        # Create deduplicated block
        block = DeduplicatedTimelineBlock(**kwargs)
        block.context_refs = current_context
        
        # Store block (without full context in content)
        block_id = await self.add_block_direct(block)
        
        # Update last context for next diff
        self.last_context = current_context
        
        return block_id
```

## Garbage Collection System

### Reference Counting and Cleanup
```python
class ContextGarbageCollector:
    """Manages cleanup of unreferenced contexts."""
    
    def __init__(self, context_store: ContextStore, timeline_repository):
        self.context_store = context_store
        self.timeline_repository = timeline_repository
    
    async def collect_garbage(self) -> Dict[str, int]:
        """Perform garbage collection of unreferenced contexts."""
        stats = {"contexts_removed": 0, "bytes_freed": 0}
        
        # Get all context hashes referenced by timeline
        referenced_hashes = await self._get_referenced_contexts()
        
        # Get all stored context hashes
        all_hashes = await self._get_all_stored_contexts()
        
        # Find unreferenced contexts
        unreferenced = all_hashes - referenced_hashes
        
        # Remove unreferenced contexts (with grace period)
        cutoff_date = datetime.now() - timedelta(days=7)  # 7-day grace period
        
        for context_hash in unreferenced:
            context_info = await self._get_context_info(context_hash)
            if context_info and context_info["last_accessed"] < cutoff_date:
                await self._remove_context(context_hash)
                stats["contexts_removed"] += 1
                stats["bytes_freed"] += context_info["size_bytes"]
        
        return stats
    
    async def _get_referenced_contexts(self) -> Set[str]:
        """Get all context hashes referenced by timeline blocks."""
        referenced = set()
        
        # Query all timeline blocks for context references
        blocks = await self.timeline_repository.get_all_blocks()
        
        for block in blocks:
            if hasattr(block, 'context_refs') and block.context_refs:
                if block.context_refs.file_system:
                    referenced.add(block.context_refs.file_system.context_hash)
                if block.context_refs.git_status:
                    referenced.add(block.context_refs.git_status.context_hash)
                # Continue for other context types...
        
        return referenced
```

## Performance Optimization

### Context Caching and Lazy Loading
```python
class ContextCache:
    """Efficient caching for frequently accessed contexts."""
    
    def __init__(self, max_size_mb: int = 50):
        self.max_size_mb = max_size_mb
        self.cache: Dict[str, Any] = {}
        self.access_times: Dict[str, datetime] = {}
        self.cache_sizes: Dict[str, int] = {}
        self.total_size = 0
    
    def get(self, context_hash: str) -> Optional[Any]:
        """Get context from cache."""
        if context_hash in self.cache:
            self.access_times[context_hash] = datetime.now()
            return self.cache[context_hash]
        return None
    
    def put(self, context_hash: str, content: Any) -> None:
        """Put context in cache with LRU eviction."""
        content_size = len(json.dumps(content).encode('utf-8'))
        
        # Evict if necessary
        while self.total_size + content_size > self.max_size_mb * 1024 * 1024:
            self._evict_lru()
        
        self.cache[context_hash] = content
        self.access_times[context_hash] = datetime.now()
        self.cache_sizes[context_hash] = content_size
        self.total_size += content_size
    
    def _evict_lru(self) -> None:
        """Evict least recently used item."""
        if not self.access_times:
            return
        
        lru_hash = min(self.access_times.items(), key=lambda x: x[1])[0]
        
        self.total_size -= self.cache_sizes[lru_hash]
        del self.cache[lru_hash]
        del self.access_times[lru_hash]
        del self.cache_sizes[lru_hash]
```

## Testing Strategy

### Unit Tests
- [ ] Content hashing consistency and collision testing
- [ ] Context deduplication accuracy
- [ ] Diff computation and application correctness
- [ ] Reference integrity maintenance

### Integration Tests
- [ ] Full timeline with context deduplication
- [ ] Context reconstruction accuracy
- [ ] Garbage collection effectiveness
- [ ] Performance improvements measurement

### Manual Testing
- [ ] Large conversation simulation with context tracking
- [ ] Database size comparison before/after deduplication
- [ ] Context reconstruction user experience
- [ ] System performance under various loads

## Documentation Updates

- [ ] Context deduplication architecture guide
- [ ] Developer guide for context-aware plugins
- [ ] Performance optimization recommendations
- [ ] Troubleshooting context reference issues

## Completion

### Final Status
- [ ] Context storage reduced by 90%+ through deduplication
- [ ] Full context reconstructable for any timeline block
- [ ] Incremental context tracking through efficient diffs
- [ ] Automatic garbage collection prevents storage bloat
- [ ] Database size grows linearly with unique content only

### Follow-up Items
- [ ] Advanced diff algorithms for specific content types
- [ ] Predictive context caching based on usage patterns
- [ ] Cross-session context sharing and deduplication
- [ ] Context compression optimization for different data types

---

*This ledger addresses the core Cursor agent problem by implementing intelligent context deduplication, preventing massive database growth while maintaining full contextual access for historical conversations.*