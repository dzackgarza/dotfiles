"""
Context Recency and Relevance Scoring

Implements Task 12.1: Intelligent scoring of conversation context based on
recency and semantic relevance to current query for optimal context management.
"""

import time
import math
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ConversationTurn:
    """Represents a single conversation turn with metadata for scoring."""
    id: str
    content: str
    role: str  # "user" or "assistant"
    timestamp: datetime
    tokens: int
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ContextScore:
    """Scoring result for a conversation turn."""
    turn_id: str
    recency_score: float  # 0.0 to 1.0
    relevance_score: float  # 0.0 to 1.0
    combined_score: float  # weighted combination
    reasoning: str  # explanation of scoring


class SimilarityCalculator(ABC):
    """Abstract base for different similarity calculation methods."""
    
    @abstractmethod
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts. Returns 0.0-1.0."""
        pass


class SimpleSimilarityCalculator(SimilarityCalculator):
    """Basic similarity calculator using word overlap and simple heuristics."""
    
    def __init__(self):
        # Common words to filter out for better relevance scoring
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'can', 'may', 'might', 'must', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'their'
        }
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity using word overlap with TF-IDF-like weighting."""
        words1 = self._extract_keywords(text1)
        words2 = self._extract_keywords(text2)
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity with frequency weighting
        intersection = set(words1.keys()) & set(words2.keys())
        union = set(words1.keys()) | set(words2.keys())
        
        if not union:
            return 0.0
        
        # Weight by frequency and inverse document frequency
        intersection_weight = sum(
            min(words1[word], words2[word]) * self._get_word_weight(word)
            for word in intersection
        )
        
        union_weight = sum(
            max(words1.get(word, 0), words2.get(word, 0)) * self._get_word_weight(word)
            for word in union
        )
        
        return intersection_weight / union_weight if union_weight > 0 else 0.0
    
    def _extract_keywords(self, text: str) -> Dict[str, int]:
        """Extract meaningful keywords with frequency counts."""
        words = text.lower().split()
        keyword_counts = {}
        
        for word in words:
            # Clean and filter
            cleaned = ''.join(c for c in word if c.isalnum())
            if len(cleaned) >= 3 and cleaned not in self.stop_words:
                keyword_counts[cleaned] = keyword_counts.get(cleaned, 0) + 1
        
        return keyword_counts
    
    def _get_word_weight(self, word: str) -> float:
        """Get importance weight for a word (longer words are more important)."""
        base_weight = 1.0
        
        # Longer words are typically more meaningful
        length_bonus = min(len(word) / 10.0, 0.5)
        
        # Technical terms (containing numbers/special patterns) get bonus
        technical_bonus = 0.2 if any(c.isdigit() for c in word) else 0.0
        
        return base_weight + length_bonus + technical_bonus


class ContextScorer:
    """
    Scores conversation turns for context relevance and recency.
    
    Implements intelligent scoring that considers both how recently something
    was said and how relevant it is to the current query.
    """
    
    def __init__(self, 
                 similarity_calculator: SimilarityCalculator = None,
                 recency_weight: float = 0.3,
                 relevance_weight: float = 0.7,
                 recency_half_life_hours: float = 24.0):
        """
        Initialize context scorer.
        
        Args:
            similarity_calculator: Method for calculating text similarity
            recency_weight: Weight for recency score (0.0-1.0)
            relevance_weight: Weight for relevance score (0.0-1.0)  
            recency_half_life_hours: Hours after which recency score halves
        """
        self.similarity_calculator = similarity_calculator or SimpleSimilarityCalculator()
        self.recency_weight = recency_weight
        self.relevance_weight = relevance_weight
        self.recency_half_life_hours = recency_half_life_hours
        
        # Normalize weights
        total_weight = recency_weight + relevance_weight
        if total_weight > 0:
            self.recency_weight /= total_weight
            self.relevance_weight /= total_weight
    
    def score_context_turns(self, 
                           turns: List[ConversationTurn],
                           current_query: str,
                           current_time: Optional[datetime] = None) -> List[ContextScore]:
        """
        Score all conversation turns for relevance to current query.
        
        Args:
            turns: List of conversation turns to score
            current_query: Current user query to score against
            current_time: Current timestamp (defaults to now)
        
        Returns:
            List of ContextScore objects, sorted by combined score (highest first)
        """
        if current_time is None:
            current_time = datetime.now(timezone.utc)
        
        scores = []
        
        for turn in turns:
            # Calculate recency score
            recency_score = self._calculate_recency_score(turn.timestamp, current_time)
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(turn.content, current_query)
            
            # Combine scores
            combined_score = (
                self.recency_weight * recency_score +
                self.relevance_weight * relevance_score
            )
            
            # Generate reasoning
            reasoning = self._generate_reasoning(turn, recency_score, relevance_score)
            
            scores.append(ContextScore(
                turn_id=turn.id,
                recency_score=recency_score,
                relevance_score=relevance_score,
                combined_score=combined_score,
                reasoning=reasoning
            ))
        
        # Sort by combined score (highest first)
        scores.sort(key=lambda s: s.combined_score, reverse=True)
        return scores
    
    def get_optimal_context(self,
                           turns: List[ConversationTurn],
                           current_query: str,
                           max_tokens: int,
                           current_time: Optional[datetime] = None) -> List[ConversationTurn]:
        """
        Select optimal subset of conversation turns for context window.
        
        Args:
            turns: Available conversation turns
            current_query: Current user query
            max_tokens: Maximum tokens allowed in context
            current_time: Current timestamp
        
        Returns:
            Optimally selected turns within token limit, in chronological order
        """
        scores = self.score_context_turns(turns, current_query, current_time)
        
        # Greedy selection by score until token limit
        selected_turns = []
        total_tokens = 0
        
        # Create turn lookup for efficiency
        turn_lookup = {turn.id: turn for turn in turns}
        
        for score in scores:
            turn = turn_lookup[score.turn_id]
            if total_tokens + turn.tokens <= max_tokens:
                selected_turns.append(turn)
                total_tokens += turn.tokens
            else:
                break
        
        # Return in chronological order for context coherence
        selected_turns.sort(key=lambda t: t.timestamp)
        return selected_turns
    
    def _calculate_recency_score(self, turn_time: datetime, current_time: datetime) -> float:
        """Calculate recency score using exponential decay."""
        time_diff_hours = (current_time - turn_time).total_seconds() / 3600.0
        
        # Exponential decay with configurable half-life
        decay_rate = math.log(2) / self.recency_half_life_hours
        recency_score = math.exp(-decay_rate * time_diff_hours)
        
        return min(recency_score, 1.0)
    
    def _calculate_relevance_score(self, turn_content: str, current_query: str) -> float:
        """Calculate semantic relevance score."""
        return self.similarity_calculator.calculate_similarity(turn_content, current_query)
    
    def _generate_reasoning(self, 
                          turn: ConversationTurn,
                          recency_score: float,
                          relevance_score: float) -> str:
        """Generate human-readable explanation of scoring."""
        recency_desc = "very recent" if recency_score > 0.8 else \
                      "recent" if recency_score > 0.5 else \
                      "somewhat old" if recency_score > 0.2 else "old"
        
        relevance_desc = "highly relevant" if relevance_score > 0.7 else \
                        "relevant" if relevance_score > 0.4 else \
                        "somewhat relevant" if relevance_score > 0.2 else "not very relevant"
        
        return f"{recency_desc} ({recency_score:.2f}) and {relevance_desc} ({relevance_score:.2f})"


class AdvancedContextScorer(ContextScorer):
    """
    Enhanced context scorer with additional heuristics for better selection.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_boundary_bonus = 0.1
        self.question_answer_pair_bonus = 0.2
    
    def score_context_turns(self, 
                           turns: List[ConversationTurn],
                           current_query: str,
                           current_time: Optional[datetime] = None) -> List[ContextScore]:
        """Enhanced scoring with conversation flow awareness."""
        base_scores = super().score_context_turns(turns, current_query, current_time)
        
        # Apply conversation flow bonuses
        enhanced_scores = []
        for i, score in enumerate(base_scores):
            turn = next(t for t in turns if t.id == score.turn_id)
            
            # Bonus for conversation boundaries (start of topics)
            boundary_bonus = self._calculate_boundary_bonus(turn, turns)
            
            # Bonus for complete question-answer pairs
            pair_bonus = self._calculate_pair_bonus(turn, turns)
            
            # Apply bonuses
            enhanced_combined = score.combined_score + boundary_bonus + pair_bonus
            enhanced_combined = min(enhanced_combined, 1.0)  # Cap at 1.0
            
            enhanced_scores.append(ContextScore(
                turn_id=score.turn_id,
                recency_score=score.recency_score,
                relevance_score=score.relevance_score,
                combined_score=enhanced_combined,
                reasoning=f"{score.reasoning}, bonuses: boundary={boundary_bonus:.2f}, pair={pair_bonus:.2f}"
            ))
        
        # Re-sort by enhanced scores
        enhanced_scores.sort(key=lambda s: s.combined_score, reverse=True)
        return enhanced_scores
    
    def _calculate_boundary_bonus(self, turn: ConversationTurn, all_turns: List[ConversationTurn]) -> float:
        """Bonus for turns that start new conversation topics."""
        # Simple heuristic: user questions often start new topics
        if turn.role == "user" and "?" in turn.content:
            return self.conversation_boundary_bonus
        return 0.0
    
    def _calculate_pair_bonus(self, turn: ConversationTurn, all_turns: List[ConversationTurn]) -> float:
        """Bonus for turns that are part of complete question-answer pairs."""
        # Find adjacent turns to see if this forms a complete pair
        turn_index = next(i for i, t in enumerate(all_turns) if t.id == turn.id)
        
        if turn.role == "user" and turn_index + 1 < len(all_turns):
            next_turn = all_turns[turn_index + 1]
            if next_turn.role == "assistant":
                return self.question_answer_pair_bonus
        
        if turn.role == "assistant" and turn_index > 0:
            prev_turn = all_turns[turn_index - 1]
            if prev_turn.role == "user":
                return self.question_answer_pair_bonus
        
        return 0.0


# Global scorer instance
default_context_scorer = ContextScorer()
advanced_context_scorer = AdvancedContextScorer()