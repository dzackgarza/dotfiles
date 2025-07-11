# Sliding Window Context System

**Branch:** feat/sliding-window-context
**Summary:** Implement sliding window context management that maintains only relevant recent context in active memory while using semantic search to retrieve historical context when needed, preventing the Cursor agent infinite context accumulation problem.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
The Cursor agent problem includes **infinite context accumulation** where every message includes full historical context, leading to massive storage and processing overhead. We need a **sliding window context system** that maintains only essential recent context while intelligently retrieving relevant historical context through semantic search when needed.

### Success Criteria
- [ ] Active context window remains bounded regardless of conversation length
- [ ] Relevant historical context is automatically retrieved when needed
- [ ] Context relevance is determined through semantic similarity
- [ ] Processing overhead scales with window size, not total history
- [ ] Context quality remains high for LLM processing

### Acceptance Criteria
- [ ] Active context never exceeds configurable token limits (default: 8K tokens)
- [ ] Historical context retrieval is transparent to users and plugins
- [ ] Semantic search finds relevant context within 100ms
- [ ] Context window adapts based on conversation complexity
- [ ] LLM performance is maintained with bounded context

## Technical Approach

### Architecture Changes
1. **Context Window Manager**: Maintains bounded active context with intelligent eviction
2. **Semantic Context Retrieval**: Finds relevant historical context through embeddings
3. **Context Relevance Scoring**: Determines which context to keep/retrieve
4. **Dynamic Window Sizing**: Adapts context window based on conversation needs
5. **Context Summarization**: Compresses older context while preserving key information

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

### Dependencies
- Context Deduplication System (for efficient historical context storage)
- LLM Integration Foundation (for embeddings and context processing)
- Sacred Timeline Persistence (for historical context access)

### Risks & Mitigations
- **Risk 1**: Important context is evicted and not retrieved semantically
  - *Mitigation*: Conservative eviction policies, relevance monitoring, manual context pinning
- **Risk 2**: Semantic retrieval is too slow for real-time conversation
  - *Mitigation*: Efficient embedding models, precomputed indices, async retrieval
- **Risk 3**: Context window is too small for complex tasks
  - *Mitigation*: Dynamic sizing, user controls, task-specific window policies

## Progress Log

### 2025-07-10 - Initial Planning
- Identified context accumulation problem in Cursor agent analysis
- Designed sliding window approach with semantic retrieval
- Created context relevance scoring and dynamic sizing strategy
- Planned integration with existing timeline and deduplication systems

## Technical Decisions

### Decision 1: Context Window Sizing Strategy
**Context**: Need to balance context richness with processing efficiency  
**Options**: Fixed size, token-based, adaptive, user-configurable  
**Decision**: Token-based with adaptive sizing and user override  
**Reasoning**: Optimal for LLM processing, adapts to conversation needs, user control  
**Consequences**: More complex but optimal context management

### Decision 2: Semantic Retrieval Approach
**Context**: Need fast, accurate retrieval of relevant historical context  
**Options**: Keyword search, embeddings, hybrid, LLM-based relevance  
**Decision**: Embedding-based with keyword fallback  
**Reasoning**: Best semantic understanding, fast retrieval, robust fallback  
**Consequences**: Requires embedding infrastructure but superior results

### Decision 3: Context Eviction Policy
**Context**: Determine which context to remove when window is full  
**Options**: LRU, time-based, relevance-based, user importance  
**Decision**: Hybrid relevance and recency scoring  
**Reasoning**: Preserves important context while maintaining freshness  
**Consequences**: More complex eviction logic but better context quality

## Sliding Window Architecture

### Context Window Manager
```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from collections import deque

@dataclass
class ContextItem:
    """Individual item in the context window."""
    content: str
    timestamp: datetime
    source_type: str  # "user", "assistant", "system", "file", "git"
    relevance_score: float = 0.0
    token_count: int = 0
    embedding: Optional[np.ndarray] = None
    importance_flags: List[str] = field(default_factory=list)  # ["user_starred", "error", "code"]
    
    def calculate_relevance(self, current_time: datetime, query_embedding: Optional[np.ndarray] = None) -> float:
        """Calculate relevance score for eviction decisions."""
        score = 0.0
        
        # Recency score (exponential decay)
        age_hours = (current_time - self.timestamp).total_seconds() / 3600
        recency_score = np.exp(-age_hours / 24.0)  # Half-life of 24 hours
        score += recency_score * 0.3
        
        # Importance flags
        importance_weights = {
            "user_starred": 0.8,
            "error": 0.6,
            "code": 0.4,
            "question": 0.5,
            "solution": 0.7
        }
        
        for flag in self.importance_flags:
            score += importance_weights.get(flag, 0.0)
        
        # Semantic similarity (if query provided)
        if query_embedding is not None and self.embedding is not None:
            similarity = np.dot(query_embedding, self.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(self.embedding)
            )
            score += similarity * 0.4
        
        # Source type bias
        source_weights = {
            "user": 0.3,
            "assistant": 0.2,
            "error": 0.4,
            "file": 0.1,
            "system": 0.1
        }
        score += source_weights.get(self.source_type, 0.0)
        
        return min(score, 1.0)

@dataclass
class ContextWindow:
    """Sliding window of active context."""
    max_tokens: int = 8000
    max_items: int = 100
    items: deque = field(default_factory=deque)
    current_tokens: int = 0
    
    def add_item(self, item: ContextItem) -> None:
        """Add item to context window, evicting if necessary."""
        self.items.append(item)
        self.current_tokens += item.token_count
        
        # Evict items if over limits
        while (self.current_tokens > self.max_tokens or 
               len(self.items) > self.max_items):
            self._evict_least_relevant()
    
    def _evict_least_relevant(self) -> Optional[ContextItem]:
        """Evict the least relevant item from the window."""
        if not self.items:
            return None
        
        # Calculate relevance scores for all items
        current_time = datetime.now()
        scored_items = [
            (i, item, item.calculate_relevance(current_time))
            for i, item in enumerate(self.items)
        ]
        
        # Sort by relevance (ascending) and evict lowest
        scored_items.sort(key=lambda x: x[2])
        
        # Don't evict items with high importance flags
        for i, item, score in scored_items:
            if "user_starred" not in item.importance_flags:
                evicted = self.items[i]
                del self.items[i]
                self.current_tokens -= evicted.token_count
                return evicted
        
        # If all items are important, evict oldest
        evicted = self.items.popleft()
        self.current_tokens -= evicted.token_count
        return evicted
    
    def get_context_for_llm(self, max_tokens: Optional[int] = None) -> str:
        """Get formatted context string for LLM."""
        target_tokens = max_tokens or self.max_tokens
        
        # Sort items by timestamp for chronological context
        sorted_items = sorted(self.items, key=lambda x: x.timestamp)
        
        context_parts = []
        used_tokens = 0
        
        for item in sorted_items:
            if used_tokens + item.token_count <= target_tokens:
                context_parts.append(f"[{item.source_type}] {item.content}")
                used_tokens += item.token_count
            else:
                break
        
        return "\n\n".join(context_parts)

class ContextWindowManager:
    """Manages sliding window context with intelligent retrieval."""
    
    def __init__(self, embedding_service, historical_retriever):
        self.embedding_service = embedding_service
        self.historical_retriever = historical_retriever
        self.context_window = ContextWindow()
        self.conversation_state = "general"  # general, coding, debugging, etc.
        
    async def add_context(self, content: str, source_type: str, 
                         importance_flags: List[str] = None) -> None:
        """Add new context to the sliding window."""
        
        # Generate embedding for semantic retrieval
        embedding = await self.embedding_service.get_embedding(content)
        
        # Count tokens (approximate)
        token_count = len(content.split()) * 1.3  # Rough token estimation
        
        # Create context item
        item = ContextItem(
            content=content,
            timestamp=datetime.now(),
            source_type=source_type,
            token_count=int(token_count),
            embedding=embedding,
            importance_flags=importance_flags or []
        )
        
        # Add to window (will evict if necessary)
        self.context_window.add_item(item)
        
        # Update conversation state based on content
        await self._update_conversation_state(content)
    
    async def get_enhanced_context(self, query: str, max_tokens: int = 8000) -> str:
        """Get context enhanced with relevant historical information."""
        
        # Get current window context
        window_context = self.context_window.get_context_for_llm(max_tokens // 2)
        
        # Get relevant historical context
        query_embedding = await self.embedding_service.get_embedding(query)
        historical_context = await self.historical_retriever.get_relevant_context(
            query_embedding, 
            max_tokens=max_tokens // 2,
            conversation_state=self.conversation_state
        )
        
        # Combine contexts
        if historical_context:
            enhanced_context = f"""# Recent Context
{window_context}

# Relevant Historical Context  
{historical_context}

# Current Query
{query}"""
        else:
            enhanced_context = f"""# Recent Context
{window_context}

# Current Query
{query}"""
        
        return enhanced_context
    
    async def _update_conversation_state(self, content: str) -> None:
        """Update conversation state based on recent content."""
        # Simple state detection - could be more sophisticated
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ["code", "function", "class", "import"]):
            self.conversation_state = "coding"
        elif any(keyword in content_lower for keyword in ["error", "bug", "debug", "fix"]):
            self.conversation_state = "debugging"
        elif any(keyword in content_lower for keyword in ["research", "find", "search", "learn"]):
            self.conversation_state = "research"
        else:
            self.conversation_state = "general"
```

### Semantic Context Retrieval
```python
import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """Generates embeddings for semantic context retrieval."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    async def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding vector for text."""
        # Clean and truncate text for embedding
        cleaned_text = self._clean_text(text)
        embedding = self.model.encode(cleaned_text)
        return embedding / np.linalg.norm(embedding)  # Normalize
    
    def _clean_text(self, text: str) -> str:
        """Clean text for better embeddings."""
        # Remove excessive whitespace and special characters
        cleaned = " ".join(text.split())
        
        # Truncate if too long (most embedding models have limits)
        if len(cleaned) > 512:
            cleaned = cleaned[:512]
        
        return cleaned

class HistoricalContextRetriever:
    """Retrieves relevant historical context using semantic search."""
    
    def __init__(self, embedding_service: EmbeddingService, 
                 context_store, timeline_repository):
        self.embedding_service = embedding_service
        self.context_store = context_store
        self.timeline_repository = timeline_repository
        
        # FAISS index for fast similarity search
        self.index = faiss.IndexFlatIP(embedding_service.dimension)
        self.context_metadata: List[Dict[str, Any]] = []
        self._index_built = False
    
    async def build_index(self) -> None:
        """Build semantic search index from historical contexts."""
        # Get all historical timeline blocks
        all_blocks = await self.timeline_repository.get_all_blocks()
        
        embeddings = []
        metadata = []
        
        for block in all_blocks:
            if block.content and len(block.content.strip()) > 10:  # Skip very short content
                try:
                    embedding = await self.embedding_service.get_embedding(block.content)
                    embeddings.append(embedding)
                    metadata.append({
                        "block_id": block.id,
                        "content": block.content,
                        "timestamp": block.timestamp,
                        "role": block.role,
                        "token_count": len(block.content.split()) * 1.3
                    })
                except Exception as e:
                    print(f"Error processing block {block.id}: {e}")
                    continue
        
        if embeddings:
            # Build FAISS index
            embedding_matrix = np.vstack(embeddings)
            self.index.add(embedding_matrix)
            self.context_metadata = metadata
            self._index_built = True
            
            print(f"Built semantic index with {len(embeddings)} contexts")
    
    async def get_relevant_context(self, query_embedding: np.ndarray,
                                 max_tokens: int = 4000,
                                 conversation_state: str = "general",
                                 top_k: int = 10) -> str:
        """Retrieve relevant historical context."""
        
        if not self._index_built:
            await self.build_index()
        
        if self.index.ntotal == 0:
            return ""
        
        # Search for similar contexts
        query_vector = query_embedding.reshape(1, -1)
        similarities, indices = self.index.search(query_vector, top_k)
        
        # Rank and filter results
        relevant_contexts = []
        total_tokens = 0
        
        for similarity, idx in zip(similarities[0], indices[0]):
            if similarity < 0.3:  # Similarity threshold
                continue
                
            metadata = self.context_metadata[idx]
            
            # Apply conversation state filtering
            if self._is_relevant_for_state(metadata, conversation_state):
                context_tokens = metadata["token_count"]
                if total_tokens + context_tokens <= max_tokens:
                    relevant_contexts.append({
                        "content": metadata["content"],
                        "similarity": similarity,
                        "timestamp": metadata["timestamp"],
                        "role": metadata["role"]
                    })
                    total_tokens += context_tokens
        
        # Sort by similarity and format
        relevant_contexts.sort(key=lambda x: x["similarity"], reverse=True)
        
        if not relevant_contexts:
            return ""
        
        # Format context for LLM
        context_parts = []
        for ctx in relevant_contexts:
            timestamp_str = ctx["timestamp"].strftime("%Y-%m-%d %H:%M")
            context_parts.append(f"[{timestamp_str}] {ctx['content'][:200]}...")
        
        return "\n\n".join(context_parts)
    
    def _is_relevant_for_state(self, metadata: Dict[str, Any], 
                              conversation_state: str) -> bool:
        """Check if context is relevant for current conversation state."""
        content = metadata["content"].lower()
        
        state_keywords = {
            "coding": ["code", "function", "class", "import", "def", "return"],
            "debugging": ["error", "bug", "debug", "fix", "exception", "traceback"],
            "research": ["research", "find", "search", "learn", "study", "analyze"],
            "general": []  # No filtering for general state
        }
        
        if conversation_state == "general":
            return True
        
        keywords = state_keywords.get(conversation_state, [])
        return any(keyword in content for keyword in keywords)
    
    async def add_to_index(self, content: str, metadata: Dict[str, Any]) -> None:
        """Add new content to the search index."""
        if not self._index_built:
            return
        
        try:
            embedding = await self.embedding_service.get_embedding(content)
            
            # Add to FAISS index
            embedding_vector = embedding.reshape(1, -1)
            self.index.add(embedding_vector)
            
            # Add metadata
            self.context_metadata.append(metadata)
            
        except Exception as e:
            print(f"Error adding to index: {e}")
```

### Dynamic Window Sizing
```python
class AdaptiveWindowManager:
    """Manages dynamic context window sizing based on conversation needs."""
    
    def __init__(self, base_window_size: int = 8000):
        self.base_window_size = base_window_size
        self.current_window_size = base_window_size
        self.conversation_complexity = 0.5  # 0.0 to 1.0
        self.task_requirements = {}
        
    def analyze_conversation_complexity(self, recent_context: List[ContextItem]) -> float:
        """Analyze recent conversation to determine complexity."""
        complexity_indicators = {
            "code_blocks": 0,
            "error_messages": 0,
            "long_messages": 0,
            "technical_terms": 0,
            "questions": 0
        }
        
        for item in recent_context[-10:]:  # Analyze last 10 items
            content = item.content.lower()
            
            # Code blocks
            if "```" in item.content:
                complexity_indicators["code_blocks"] += 1
            
            # Error messages
            if any(term in content for term in ["error", "exception", "traceback", "failed"]):
                complexity_indicators["error_messages"] += 1
            
            # Long messages (indicate complex topics)
            if len(item.content) > 500:
                complexity_indicators["long_messages"] += 1
            
            # Technical terms
            tech_terms = ["algorithm", "implementation", "architecture", "database", "api"]
            if any(term in content for term in tech_terms):
                complexity_indicators["technical_terms"] += 1
            
            # Questions
            if "?" in item.content:
                complexity_indicators["questions"] += 1
        
        # Calculate complexity score
        total_indicators = sum(complexity_indicators.values())
        max_possible = len(recent_context[-10:]) * 2  # Max 2 indicators per item
        
        return min(total_indicators / max_possible, 1.0) if max_possible > 0 else 0.0
    
    def adjust_window_size(self, complexity: float, task_type: str = "general") -> int:
        """Adjust window size based on complexity and task type."""
        
        # Base adjustments for task type
        task_multipliers = {
            "general": 1.0,
            "coding": 1.5,
            "debugging": 2.0,
            "research": 1.3,
            "complex_analysis": 2.5
        }
        
        task_multiplier = task_multipliers.get(task_type, 1.0)
        
        # Complexity adjustment (0.5x to 3.0x)
        complexity_multiplier = 0.5 + (complexity * 2.5)
        
        # Calculate new window size
        new_size = int(self.base_window_size * task_multiplier * complexity_multiplier)
        
        # Apply reasonable bounds
        min_size = self.base_window_size // 2
        max_size = self.base_window_size * 4
        
        return max(min_size, min(new_size, max_size))
    
    def get_recommended_window_size(self, recent_context: List[ContextItem],
                                  current_task: str = "general") -> int:
        """Get recommended window size for current conversation state."""
        
        # Analyze current complexity
        complexity = self.analyze_conversation_complexity(recent_context)
        
        # Adjust size
        recommended_size = self.adjust_window_size(complexity, current_task)
        
        # Smooth transitions (don't change size too dramatically)
        size_change = abs(recommended_size - self.current_window_size)
        max_change = self.base_window_size // 4
        
        if size_change > max_change:
            if recommended_size > self.current_window_size:
                new_size = self.current_window_size + max_change
            else:
                new_size = self.current_window_size - max_change
        else:
            new_size = recommended_size
        
        self.current_window_size = new_size
        self.conversation_complexity = complexity
        
        return new_size
```

### Integration with Timeline System
```python
class SlidingWindowTimeline(SacredTimeline):
    """Timeline with sliding window context management."""
    
    def __init__(self, embedding_service: EmbeddingService):
        super().__init__()
        self.context_manager = ContextWindowManager(
            embedding_service, 
            HistoricalContextRetriever(embedding_service, None, self)
        )
        self.adaptive_manager = AdaptiveWindowManager()
    
    async def add_block_with_context_management(self, **kwargs) -> str:
        """Add block with automatic context window management."""
        
        # Add block to timeline
        block_id = await self.add_block(**kwargs)
        
        # Add to context window
        content = kwargs.get("content", "")
        role = kwargs.get("role", "unknown")
        
        importance_flags = []
        if "error" in content.lower():
            importance_flags.append("error")
        if "```" in content:
            importance_flags.append("code")
        
        await self.context_manager.add_context(
            content=content,
            source_type=role,
            importance_flags=importance_flags
        )
        
        # Adjust window size if needed
        recent_context = list(self.context_manager.context_window.items)
        new_window_size = self.adaptive_manager.get_recommended_window_size(
            recent_context, 
            self.context_manager.conversation_state
        )
        
        if new_window_size != self.context_manager.context_window.max_tokens:
            self.context_manager.context_window.max_tokens = new_window_size
            print(f"Adjusted context window to {new_window_size} tokens "
                  f"(complexity: {self.adaptive_manager.conversation_complexity:.2f})")
        
        return block_id
    
    async def get_context_for_query(self, query: str, max_tokens: int = None) -> str:
        """Get optimized context for LLM query."""
        
        # Use adaptive window size if not specified
        if max_tokens is None:
            max_tokens = self.context_manager.context_window.max_tokens
        
        # Get enhanced context with historical retrieval
        context = await self.context_manager.get_enhanced_context(query, max_tokens)
        
        return context
```

## Testing Strategy

### Unit Tests
- [ ] Context window eviction policies
- [ ] Semantic similarity calculations  
- [ ] Dynamic window sizing algorithms
- [ ] Context relevance scoring

### Integration Tests
- [ ] Full conversation with sliding window management
- [ ] Historical context retrieval accuracy
- [ ] Performance with large historical datasets
- [ ] Window size adaptation behavior

### Manual Testing
- [ ] Long conversations to test window management
- [ ] Complex technical discussions requiring historical context
- [ ] Performance comparison with fixed context approaches
- [ ] User experience with transparent context management

## Documentation Updates

- [ ] Sliding window context architecture guide
- [ ] Semantic retrieval system documentation
- [ ] Configuration guide for window sizing and policies
- [ ] Performance tuning recommendations

## Completion

### Final Status
- [ ] Active context window remains bounded regardless of conversation length
- [ ] Relevant historical context retrieved transparently
- [ ] Processing overhead scales with window size, not total history
- [ ] Dynamic window sizing adapts to conversation complexity
- [ ] LLM performance maintained with optimal context

### Follow-up Items
- [ ] Advanced conversation state detection
- [ ] User-specific context preferences and patterns
- [ ] Cross-conversation context sharing
- [ ] Context quality metrics and optimization

---

*This ledger implements sliding window context management to solve the Cursor agent infinite context accumulation problem while maintaining high-quality contextual AI interactions.*