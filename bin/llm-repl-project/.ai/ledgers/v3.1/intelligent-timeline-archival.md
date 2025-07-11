# Intelligent Timeline Archival System

**Branch:** feat/intelligent-timeline-archival
**Summary:** Implement intelligent archival and pruning strategies for the Sacred Timeline to prevent database bloat while maintaining accessibility to historical context and avoiding the Cursor/VSCode agent problem of accumulating massive databases.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
The Sacred Timeline persistence system risks the **Cursor Agent Problem**: accumulating massive databases (500+ MB) from storing every conversation, file context, and state change. Unlike Cursor which becomes sluggish and requires periodic manual cleaning, we need **intelligent archival strategies** that maintain long-term accessibility while preventing performance degradation.

### Success Criteria
- [ ] Timeline database remains performant regardless of usage duration
- [ ] Historical context remains accessible through intelligent retrieval
- [ ] Automatic archival prevents manual database maintenance
- [ ] User can access any historical conversation efficiently
- [ ] System scales gracefully from weeks to years of usage

### Acceptance Criteria
- [ ] Active database never exceeds configurable size limits (default: 100MB)
- [ ] Archived data remains searchable and retrievable
- [ ] Archival is transparent to users (no manual intervention required)
- [ ] Historical context can be restored to active memory when needed
- [ ] Performance remains consistent regardless of total history size

## Technical Approach

### Architecture Changes
1. **Hierarchical Storage Tiers**: Hot, warm, and cold data storage with automatic migration
2. **Intelligent Context Pruning**: Smart compression and deduplication of historical data
3. **Semantic Indexing**: Enable efficient search and retrieval of archived content
4. **Automatic Lifecycle Management**: Time and size-based archival policies
5. **On-Demand Restoration**: Transparent access to archived conversations

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

### Dependencies
- Sacred Timeline Persistence (base timeline storage system)
- Plugin Architecture Foundation (archival as plugin)
- LLM Integration Foundation (for semantic summarization)

### Risks & Mitigations
- **Risk 1**: Archived data becomes inaccessible or corrupted
  - *Mitigation*: Multiple archival formats, integrity checking, recovery procedures
- **Risk 2**: Archival process impacts performance
  - *Mitigation*: Background processing, incremental archival, user-configurable timing
- **Risk 3**: Important context is lost during archival
  - *Mitigation*: Smart preservation rules, user input on important conversations, rollback capability

## Progress Log

### 2025-07-10 - Initial Planning
- Identified Cursor agent problem and need for intelligent archival
- Analyzed hierarchical storage strategies for timeline data
- Designed automatic archival policies and user controls
- Created retrieval and restoration system architecture

## Technical Decisions

### Decision 1: Storage Tier Strategy
**Context**: Need efficient storage hierarchy preventing database bloat  
**Options**: Time-based tiers, size-based tiers, usage-based tiers, hybrid approach  
**Decision**: Hybrid time and usage-based tiers with configurable policies  
**Reasoning**: Balances recency with importance, allows user customization  
**Consequences**: More complex but optimal for different usage patterns

### Decision 2: Archival Compression Strategy
**Context**: Archived data should be compact but searchable  
**Options**: Full compression, semantic summarization, deduplication, hybrid  
**Decision**: Semantic summarization with deduplication and compression  
**Reasoning**: Maintains searchability while achieving high compression ratios  
**Consequences**: Higher processing cost but much better space efficiency

### Decision 3: Retrieval Interface Design
**Context**: Users need access to archived data without complexity  
**Options**: Separate archive view, integrated search, automatic restoration, manual export  
**Decision**: Integrated search with automatic restoration to active timeline  
**Reasoning**: Seamless user experience, archived data feels accessible  
**Consequences**: More complex implementation but transparent to users

## Storage Hierarchy Architecture

### Tier Definitions
```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class StorageTier(Enum):
    HOT = "hot"        # Active database - instant access
    WARM = "warm"      # Compressed local files - fast access  
    COLD = "cold"      # Archived files - background access

@dataclass
class ArchivalPolicy:
    """Defines when and how data moves between storage tiers."""
    
    # Hot → Warm transition
    hot_max_age: timedelta = timedelta(days=7)
    hot_max_size_mb: int = 50
    hot_max_conversations: int = 100
    
    # Warm → Cold transition
    warm_max_age: timedelta = timedelta(days=30)
    warm_max_size_mb: int = 200
    
    # Cold storage management
    cold_max_age: Optional[timedelta] = None  # Never delete
    cold_compression_level: int = 9
    
    # Preservation rules
    preserve_starred_conversations: bool = True
    preserve_error_conversations: bool = True
    preserve_long_conversations: bool = True  # >50 blocks
    min_preserve_per_day: int = 1  # Always keep at least 1 conversation per day

class TierManager:
    """Manages data movement between storage tiers."""
    
    def __init__(self, policy: ArchivalPolicy):
        self.policy = policy
        self.hot_storage = HotStorage()      # SQLite database
        self.warm_storage = WarmStorage()    # Compressed JSON files
        self.cold_storage = ColdStorage()    # Archived compressed files
    
    async def check_and_migrate(self) -> ArchivalStats:
        """Check all tiers and migrate data according to policy."""
        stats = ArchivalStats()
        
        # Check hot storage for migration to warm
        hot_candidates = await self._identify_hot_migration_candidates()
        for session_id in hot_candidates:
            await self._migrate_hot_to_warm(session_id)
            stats.hot_to_warm_count += 1
        
        # Check warm storage for migration to cold
        warm_candidates = await self._identify_warm_migration_candidates()
        for archive_id in warm_candidates:
            await self._migrate_warm_to_cold(archive_id)
            stats.warm_to_cold_count += 1
        
        return stats
    
    async def _identify_hot_migration_candidates(self) -> List[str]:
        """Identify sessions that should move from hot to warm storage."""
        candidates = []
        
        # Get all sessions in hot storage
        sessions = await self.hot_storage.get_all_sessions()
        
        for session in sessions:
            should_migrate = False
            
            # Check age
            age = datetime.now() - session.last_activity
            if age > self.policy.hot_max_age:
                should_migrate = True
            
            # Check if not in preservation rules
            if not self._should_preserve_in_hot(session):
                should_migrate = True
            
            if should_migrate:
                candidates.append(session.id)
        
        # Ensure we don't exceed size limits
        if await self.hot_storage.get_size_mb() > self.policy.hot_max_size_mb:
            # Add oldest sessions until under limit
            oldest_sessions = await self.hot_storage.get_sessions_by_age()
            for session in oldest_sessions:
                if session.id not in candidates:
                    candidates.append(session.id)
                if await self.hot_storage.get_size_mb() <= self.policy.hot_max_size_mb:
                    break
        
        return candidates
```

### Hot Storage (Active Database)
```python
class HotStorage:
    """Fast SQLite database for active timeline data."""
    
    def __init__(self, db_path: str = "timeline_hot.db"):
        self.db_path = db_path
        self.connection_pool = SQLitePool(db_path)
    
    async def get_size_mb(self) -> float:
        """Get current database size in MB."""
        return os.path.getsize(self.db_path) / (1024 * 1024)
    
    async def vacuum_and_optimize(self) -> None:
        """Optimize hot storage after archival operations."""
        async with self.connection_pool.acquire() as conn:
            await conn.execute("VACUUM")
            await conn.execute("ANALYZE")
            await conn.execute("PRAGMA optimize")
    
    async def get_storage_statistics(self) -> Dict[str, Any]:
        """Get detailed storage statistics for monitoring."""
        async with self.connection_pool.acquire() as conn:
            stats = {}
            
            # Session counts
            stats["total_sessions"] = await conn.fetchval("SELECT COUNT(*) FROM timeline_sessions")
            stats["total_blocks"] = await conn.fetchval("SELECT COUNT(*) FROM timeline_blocks")
            stats["total_sub_blocks"] = await conn.fetchval("SELECT COUNT(*) FROM timeline_sub_blocks")
            
            # Size distribution
            stats["avg_session_size"] = await conn.fetchval("""
                SELECT AVG(LENGTH(content)) FROM timeline_blocks
            """)
            
            # Age distribution
            stats["oldest_session"] = await conn.fetchval("""
                SELECT MIN(created_at) FROM timeline_sessions
            """)
            stats["newest_session"] = await conn.fetchval("""
                SELECT MAX(updated_at) FROM timeline_sessions
            """)
            
            return stats
```

### Warm Storage (Compressed Local Files)
```python
class WarmStorage:
    """Compressed JSON files for medium-term storage."""
    
    def __init__(self, storage_dir: Path = Path("timeline_warm")):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.index_file = storage_dir / "index.json"
        self._load_index()
    
    async def archive_session(self, session_data: TimelineSession) -> str:
        """Archive a session to warm storage with compression."""
        archive_id = f"{session_data.id}_{int(datetime.now().timestamp())}"
        
        # Create compressed archive
        compressed_data = await self._compress_session(session_data)
        
        # Generate semantic summary for searchability
        summary = await self._generate_session_summary(session_data)
        
        # Store archive file
        archive_path = self.storage_dir / f"{archive_id}.gz"
        with gzip.open(archive_path, 'wb') as f:
            f.write(compressed_data)
        
        # Update index
        self.index[archive_id] = {
            "original_session_id": session_data.id,
            "created_at": session_data.created_at.isoformat(),
            "archived_at": datetime.now().isoformat(),
            "block_count": len(session_data.blocks),
            "summary": summary,
            "file_size": archive_path.stat().st_size,
            "keywords": self._extract_keywords(session_data)
        }
        await self._save_index()
        
        return archive_id
    
    async def _compress_session(self, session: TimelineSession) -> bytes:
        """Compress session data with deduplication."""
        # Convert to serializable format
        session_dict = {
            "session": session.to_dict(),
            "blocks": [block.to_dict() for block in session.blocks]
        }
        
        # Apply content deduplication
        deduplicated_dict = self._deduplicate_content(session_dict)
        
        # Serialize and compress
        json_data = json.dumps(deduplicated_dict, separators=(',', ':')).encode('utf-8')
        return gzip.compress(json_data, compresslevel=6)
    
    async def _generate_session_summary(self, session: TimelineSession) -> str:
        """Generate semantic summary of session for search indexing."""
        # Collect key content from session
        user_queries = []
        assistant_responses = []
        
        for block in session.blocks[:10]:  # Summarize first 10 blocks
            if block.role == "user":
                user_queries.append(block.content[:200])
            elif block.role == "assistant":
                assistant_responses.append(block.content[:200])
        
        # Use LLM to generate summary (if available)
        if hasattr(self, 'llm_provider'):
            summary_request = LLMRequest(
                messages=[{
                    "role": "user", 
                    "content": f"Summarize this conversation in 2-3 sentences:\n"
                              f"User queries: {user_queries}\n"
                              f"Responses: {assistant_responses}"
                }],
                model="tinyllama",
                max_tokens=100,
                temperature=0.1
            )
            
            try:
                response = await self.llm_provider.make_request(summary_request)
                return response.content
            except Exception:
                pass
        
        # Fallback to simple summary
        topics = set()
        for query in user_queries:
            topics.update(self._extract_keywords([query]))
        
        return f"Conversation about: {', '.join(list(topics)[:5])}"
    
    def _deduplicate_content(self, session_dict: Dict) -> Dict:
        """Remove duplicate content within session."""
        content_hashes = {}
        deduplicated = session_dict.copy()
        
        for block in deduplicated["blocks"]:
            content = block.get("content", "")
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            if content_hash in content_hashes:
                # Replace with reference to first occurrence
                block["content"] = f"@dedup:{content_hash}"
                block["content_deduped"] = True
            else:
                content_hashes[content_hash] = content
        
        # Store content lookup table
        deduplicated["content_lookup"] = content_hashes
        
        return deduplicated
```

### Cold Storage (Long-term Archives)
```python
class ColdStorage:
    """Long-term compressed archives with metadata indexing."""
    
    def __init__(self, storage_dir: Path = Path("timeline_cold")):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.metadata_db = storage_dir / "metadata.db"
        self._init_metadata_db()
    
    async def archive_from_warm(self, warm_archive_id: str, 
                               warm_data: bytes) -> str:
        """Move archive from warm to cold storage with additional compression."""
        cold_archive_id = f"cold_{warm_archive_id}"
        
        # Super-compress for long-term storage
        super_compressed = lzma.compress(warm_data, preset=9)
        
        # Store in cold storage
        cold_path = self.storage_dir / f"{cold_archive_id}.xz"
        with open(cold_path, 'wb') as f:
            f.write(super_compressed)
        
        # Update metadata database
        await self._store_cold_metadata(cold_archive_id, warm_archive_id, cold_path)
        
        return cold_archive_id
    
    async def search_archives(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search archived conversations by content."""
        # Search metadata database
        search_results = await self._search_metadata(query, limit)
        
        return search_results
    
    async def restore_archive(self, archive_id: str) -> Optional[TimelineSession]:
        """Restore an archived session to memory."""
        # Get archive metadata
        metadata = await self._get_archive_metadata(archive_id)
        if not metadata:
            return None
        
        # Load and decompress archive
        archive_path = Path(metadata["file_path"])
        if not archive_path.exists():
            return None
        
        with open(archive_path, 'rb') as f:
            compressed_data = f.read()
        
        # Decompress (handle both gzip and lzma)
        if archive_path.suffix == '.xz':
            decompressed_data = lzma.decompress(compressed_data)
        else:
            decompressed_data = gzip.decompress(compressed_data)
        
        # Parse session data
        session_dict = json.loads(decompressed_data.decode('utf-8'))
        
        # Reconstruct deduplicated content
        session_dict = self._restore_deduplicated_content(session_dict)
        
        # Convert back to TimelineSession object
        return TimelineSession.from_dict(session_dict)
```

## Intelligent Archival Strategies

### Content-Aware Preservation
```python
class ConversationAnalyzer:
    """Analyzes conversations to determine archival priority."""
    
    def analyze_session_importance(self, session: TimelineSession) -> ImportanceScore:
        """Calculate importance score for preservation decisions."""
        score = ImportanceScore()
        
        # Length-based scoring
        if len(session.blocks) > 50:
            score.add_factor("length", 0.3, "Long conversation")
        
        # Error/debugging sessions are important
        error_blocks = [b for b in session.blocks if "error" in b.content.lower()]
        if error_blocks:
            score.add_factor("errors", 0.4, "Contains error information")
        
        # Code-related conversations
        code_blocks = [b for b in session.blocks if "```" in b.content]
        if len(code_blocks) > 3:
            score.add_factor("code", 0.3, "Contains significant code")
        
        # User-starred or flagged
        if session.metadata.get("starred", False):
            score.add_factor("starred", 0.8, "User-starred conversation")
        
        # Recency bonus
        age = datetime.now() - session.last_activity
        if age < timedelta(hours=24):
            score.add_factor("recent", 0.2, "Recent activity")
        
        return score

@dataclass
class ImportanceScore:
    total_score: float = 0.0
    factors: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_factor(self, name: str, weight: float, reason: str) -> None:
        self.factors.append({"name": name, "weight": weight, "reason": reason})
        self.total_score += weight
    
    def should_preserve_in_hot(self) -> bool:
        return self.total_score > 0.5
    
    def should_preserve_in_warm(self) -> bool:
        return self.total_score > 0.3
```

### Automatic Lifecycle Management
```python
class ArchivalScheduler:
    """Schedules and executes automatic archival operations."""
    
    def __init__(self, tier_manager: TierManager):
        self.tier_manager = tier_manager
        self.scheduler = AsyncIOScheduler()
        self._setup_scheduled_tasks()
    
    def _setup_scheduled_tasks(self) -> None:
        """Setup automatic archival tasks."""
        
        # Hourly: Check for immediate archival needs
        self.scheduler.add_job(
            self._quick_archival_check,
            'interval',
            hours=1,
            id='quick_archival'
        )
        
        # Daily: Full archival cycle
        self.scheduler.add_job(
            self._full_archival_cycle,
            'cron',
            hour=2,  # 2 AM
            id='daily_archival'
        )
        
        # Weekly: Deep cleanup and optimization
        self.scheduler.add_job(
            self._deep_cleanup,
            'cron',
            day_of_week=0,  # Sunday
            hour=3,  # 3 AM
            id='weekly_cleanup'
        )
    
    async def _quick_archival_check(self) -> None:
        """Quick check for urgent archival needs."""
        hot_size = await self.tier_manager.hot_storage.get_size_mb()
        
        if hot_size > self.tier_manager.policy.hot_max_size_mb * 0.8:
            # Approaching size limit, archive oldest sessions
            await self.tier_manager.check_and_migrate()
    
    async def _full_archival_cycle(self) -> None:
        """Complete archival cycle with all optimizations."""
        # Perform archival
        stats = await self.tier_manager.check_and_migrate()
        
        # Optimize hot storage
        await self.tier_manager.hot_storage.vacuum_and_optimize()
        
        # Log archival statistics
        logger.info(f"Archival completed: {stats.hot_to_warm_count} sessions to warm, "
                   f"{stats.warm_to_cold_count} archives to cold")
    
    async def _deep_cleanup(self) -> None:
        """Weekly deep cleanup and optimization."""
        # Full archival cycle
        await self._full_archival_cycle()
        
        # Rebuild search indexes
        await self.tier_manager.cold_storage.rebuild_search_index()
        
        # Check for corruption
        await self._verify_archive_integrity()
```

## User Interface Integration

### Archival Status and Controls
```python
class ArchivalStatusWidget(Widget):
    """Widget showing archival status and user controls."""
    
    def __init__(self, tier_manager: TierManager):
        super().__init__()
        self.tier_manager = tier_manager
    
    def compose(self) -> ComposeResult:
        yield Static("Timeline Storage", classes="header")
        yield Container(
            Static("Hot (Active): ", classes="label"),
            Static(id="hot-status"),
            Static("Warm (Recent): ", classes="label"),
            Static(id="warm-status"),
            Static("Cold (Archived): ", classes="label"),
            Static(id="cold-status"),
            classes="storage-status"
        )
        yield Button("Archive Now", id="archive-now")
        yield Button("Search Archives", id="search-archives")
    
    async def update_status(self) -> None:
        """Update storage status display."""
        hot_stats = await self.tier_manager.hot_storage.get_storage_statistics()
        warm_stats = await self.tier_manager.warm_storage.get_statistics()
        cold_stats = await self.tier_manager.cold_storage.get_statistics()
        
        self.query_one("#hot-status").update(
            f"{hot_stats['total_sessions']} sessions, "
            f"{hot_stats['size_mb']:.1f} MB"
        )
        
        self.query_one("#warm-status").update(
            f"{warm_stats['archive_count']} archives, "
            f"{warm_stats['size_mb']:.1f} MB"
        )
        
        self.query_one("#cold-status").update(
            f"{cold_stats['archive_count']} archives, "
            f"{cold_stats['size_mb']:.1f} MB"
        )

class ArchiveSearchWidget(Widget):
    """Widget for searching and restoring archived conversations."""
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search archived conversations...", id="search-input")
        yield DataTable(id="search-results")
        yield Button("Restore Selected", id="restore-button")
    
    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if len(event.value) >= 3:  # Start searching after 3 characters
            results = await self.tier_manager.cold_storage.search_archives(event.value)
            await self._display_search_results(results)
```

## Testing Strategy

### Unit Tests
- [ ] Storage tier migration logic
- [ ] Compression and deduplication algorithms  
- [ ] Search and retrieval functionality
- [ ] Archival policy enforcement

### Integration Tests
- [ ] Full archival lifecycle with real timeline data
- [ ] Performance testing with large datasets
- [ ] Archive corruption and recovery scenarios
- [ ] Cross-tier data consistency

### Manual Testing
- [ ] Long-running usage simulation
- [ ] Archive search and restoration user experience
- [ ] Performance under various archival policies
- [ ] Database size monitoring and alerting

## Documentation Updates

- [ ] Archival system architecture and policies
- [ ] User guide for archive management
- [ ] Performance tuning and configuration guide
- [ ] Troubleshooting archive corruption and recovery

## Performance Considerations

### Archival Performance
- Background processing to avoid blocking UI
- Incremental archival to spread processing load
- Intelligent scheduling based on system activity
- Progress monitoring and user feedback

### Retrieval Performance  
- Efficient search indexing for archived content
- Lazy loading of archive contents
- Caching of frequently accessed archives
- Parallel processing for bulk operations

## Completion

### Final Status
- [ ] Hierarchical storage system prevents database bloat
- [ ] Automatic archival maintains optimal performance
- [ ] Historical conversations remain accessible through search
- [ ] User controls provide transparency and customization
- [ ] System scales gracefully with long-term usage

### Follow-up Items
- [ ] Machine learning-based importance scoring
- [ ] Cross-device archive synchronization
- [ ] Advanced search with semantic similarity
- [ ] Archive analytics and usage insights

---

*This ledger tracks the implementation of intelligent timeline archival to solve the Cursor agent problem and ensure sustainable long-term timeline growth without performance degradation.*