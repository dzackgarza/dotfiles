# Sacred Timeline Persistence

**Branch:** feat/sacred-timeline-persistence
**Summary:** Transform V3-minimal's in-memory timeline into a true persistent, append-only Sacred Timeline database that preserves conversation history across sessions.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal violates the core Sacred Timeline principle by keeping the timeline **IN-MEMORY ONLY**. The original design specifies "The Sacred Timeline (Database): A persistent, append-only log that stores the final, inscribed state of every block from every turn." Without persistence, the timeline is not truly "sacred" - it's ephemeral and loses all context between sessions.

### Success Criteria
- [ ] Timeline persists across application restarts
- [ ] Append-only immutable log maintained on disk
- [ ] Complete conversation history preserved
- [ ] Fast startup with timeline restoration
- [ ] Atomic writes prevent corruption

### Acceptance Criteria
- [ ] User can close and reopen app with full timeline intact
- [ ] Timeline data survives system crashes/power failures
- [ ] Historical context available for LLM processing
- [ ] Timeline file format is human-readable and debuggable
- [ ] Performance remains acceptable with large timelines

## Technical Approach

### Architecture Changes
1. **Persistent Storage Layer**: SQLite database for timeline blocks
2. **Timeline Repository**: Data access layer abstracting storage
3. **Session Management**: Timeline sessions with unique identifiers
4. **Atomic Operations**: Transaction-based writes preventing corruption
5. **Migration System**: Schema evolution for future changes

### Implementation Plan
1. **Phase 1: Storage Foundation**
   - Design timeline database schema
   - Create `TimelineRepository` with CRUD operations
   - Implement atomic write operations with transactions

2. **Phase 2: Persistence Integration**
   - Modify `SacredTimeline` to use persistent storage
   - Add timeline restoration on application startup
   - Implement incremental timeline loading

3. **Phase 3: Session Management**
   - Add timeline session concepts
   - Implement session switching and management
   - Add timeline export/import capabilities

4. **Phase 4: Performance Optimization**
   - Add timeline indexing for fast queries
   - Implement lazy loading for large timelines
   - Add timeline archiving for old sessions

### Dependencies
- Plugin Validator System (for proper block validation before persistence)
- LLM Integration (for real token tracking in persisted data)

### Risks & Mitigations
- **Risk 1**: Timeline corruption from incomplete writes
  - *Mitigation*: Atomic transactions, write-ahead logging, integrity checks
- **Risk 2**: Performance degradation with large timelines
  - *Mitigation*: Pagination, indexing, lazy loading strategies
- **Risk 3**: Migration complexity for schema changes
  - *Mitigation*: Versioned schema with automated migration scripts

## Progress Log

### 2025-07-10 - Initial Planning
- Identified Sacred Timeline persistence violation in V3-minimal
- Analyzed storage requirements for timeline blocks
- Designed database schema for persistent timeline
- Created implementation roadmap

## Technical Decisions

### Decision 1: SQLite vs JSON File Storage
**Context**: Need reliable, atomic persistence for timeline data  
**Options**: JSON files, SQLite database, PostgreSQL, custom binary format  
**Decision**: SQLite database with JSON column for metadata  
**Reasoning**: ACID transactions, excellent Python support, human-readable with sqlite3 CLI  
**Consequences**: Robust persistence with SQL query capabilities

### Decision 2: Schema Design Strategy
**Context**: Timeline blocks have complex nested structure with sub-blocks  
**Options**: Flat table, normalized relations, JSON documents, hybrid approach  
**Decision**: Hybrid - core fields in columns, metadata/content as JSON  
**Reasoning**: Structured queries on core fields, flexibility for metadata evolution  
**Consequences**: Best of both worlds - performance and flexibility

### Decision 3: Session Management Model
**Context**: Users need multiple timeline sessions for different projects  
**Options**: Single global timeline, session-based timelines, workspace model  
**Decision**: Session-based timelines with current session concept  
**Reasoning**: Aligns with user mental model of different conversation threads  
**Consequences**: More complex but more useful for real workflows

## Database Schema

### Timeline Sessions
```sql
CREATE TABLE timeline_sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON
);
```

### Timeline Blocks  
```sql
CREATE TABLE timeline_blocks (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    time_taken REAL,
    tokens_input INTEGER,
    tokens_output INTEGER,
    metadata JSON,
    FOREIGN KEY (session_id) REFERENCES timeline_sessions(id)
);
```

### Sub-blocks
```sql
CREATE TABLE timeline_sub_blocks (
    id TEXT PRIMARY KEY,
    block_id TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (block_id) REFERENCES timeline_blocks(id)
);
```

## Testing Strategy

### Unit Tests
- [ ] Timeline repository CRUD operations
- [ ] Atomic transaction handling
- [ ] Schema migration functionality
- [ ] Timeline restoration from database

### Integration Tests
- [ ] Full timeline persistence through app lifecycle
- [ ] Session switching and management
- [ ] Large timeline performance
- [ ] Corruption recovery scenarios

### Manual Testing
- [ ] App restart with timeline restoration
- [ ] Timeline export/import functionality
- [ ] Session creation and switching
- [ ] Database integrity after crashes

## Performance Considerations

### Query Optimization
- Index on `(session_id, timestamp)` for chronological queries
- Index on `role` for filtering by block type
- Partial index on `tokens_input IS NOT NULL` for LLM blocks

### Memory Management
- Lazy loading of timeline blocks (load window around current position)
- Configurable timeline window size
- Background archiving of old sessions

### Storage Efficiency
- VACUUM operations for database maintenance
- JSON compression for large metadata
- Optional timeline compaction for old sessions

## Documentation Updates

- [ ] Timeline persistence architecture guide
- [ ] Database schema documentation
- [ ] Session management user guide
- [ ] Timeline export/import documentation

## Core Implementation Components

### TimelineRepository Interface
```python
class TimelineRepository:
    def create_session(self, name: str) -> TimelineSession
    def get_session(self, session_id: str) -> TimelineSession
    def list_sessions(self) -> List[TimelineSession]
    def add_block(self, session_id: str, block: TimelineBlock) -> bool
    def get_blocks(self, session_id: str, limit: int = None) -> List[TimelineBlock]
    def export_session(self, session_id: str) -> dict
    def import_session(self, data: dict) -> TimelineSession
```

### SacredTimeline Integration
```python
class SacredTimeline:
    def __init__(self, repository: TimelineRepository):
        self._repository = repository
        self._current_session: Optional[TimelineSession] = None
    
    def switch_session(self, session_id: str) -> None
    def add_block(self, **kwargs) -> None  # Persists immediately
    def get_blocks(self) -> List[TimelineBlock]  # From current session
```

## Migration Strategy

### V3-minimal Migration
1. Create database schema
2. Add compatibility layer for existing in-memory timeline
3. Gradually migrate timeline operations to persistent storage
4. Remove in-memory timeline once persistence proven stable

### Data Migration
- Export existing timeline data before migration
- Automated migration scripts for schema changes
- Rollback capability for failed migrations

## Completion

### Final Status
- [ ] Sacred Timeline properly persisted to database
- [ ] Session management fully functional
- [ ] Timeline restoration working on app startup
- [ ] Performance acceptable for large timelines
- [ ] Migration from V3-minimal complete

### Follow-up Items
- [ ] Timeline search and filtering capabilities
- [ ] Timeline analytics and statistics
- [ ] Cloud synchronization support
- [ ] Timeline sharing and collaboration

---

*This ledger tracks the transformation of V3-minimal's ephemeral timeline into a true persistent Sacred Timeline database.*

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system
