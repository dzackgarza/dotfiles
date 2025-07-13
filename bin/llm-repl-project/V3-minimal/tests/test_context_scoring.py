"""
Tests for Context Recency and Relevance Scoring

Validates Task 12.1 implementation with real scenarios.
"""

import pytest
from datetime import datetime, timezone, timedelta
from src.core.context_scoring import (
    ConversationTurn,
    ContextScore,
    ContextScorer,
    SimpleSimilarityCalculator,
    AdvancedContextScorer
)


class TestSimpleSimilarityCalculator:
    """Test basic similarity calculation."""
    
    def setup_method(self):
        self.calculator = SimpleSimilarityCalculator()
    
    def test_identical_texts(self):
        """Identical texts should have high similarity."""
        text = "How do I implement machine learning algorithms?"
        similarity = self.calculator.calculate_similarity(text, text)
        assert similarity > 0.9
    
    def test_completely_different_texts(self):
        """Completely different texts should have low similarity."""
        text1 = "What's the weather like today?"
        text2 = "How do I cook pasta properly?"
        similarity = self.calculator.calculate_similarity(text1, text2)
        assert similarity < 0.3
    
    def test_related_texts(self):
        """Related texts should have moderate similarity."""
        text1 = "How do I train a neural network?"
        text2 = "What are the best practices for machine learning?"
        similarity = self.calculator.calculate_similarity(text1, text2)
        assert 0.3 < similarity < 0.8
    
    def test_empty_texts(self):
        """Empty texts should have zero similarity."""
        assert self.calculator.calculate_similarity("", "test") == 0.0
        assert self.calculator.calculate_similarity("test", "") == 0.0
        assert self.calculator.calculate_similarity("", "") == 0.0


class TestContextScorer:
    """Test context scoring functionality."""
    
    def setup_method(self):
        self.scorer = ContextScorer(recency_half_life_hours=24.0)
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str, hours_ago: float, tokens: int = 50) -> ConversationTurn:
        """Helper to create test conversation turns."""
        timestamp = self.current_time - timedelta(hours=hours_ago)
        return ConversationTurn(
            id=f"turn_{len(content)}_{hours_ago}",
            content=content,
            role=role,
            timestamp=timestamp,
            tokens=tokens
        )
    
    def test_recency_scoring(self):
        """Test that recent turns score higher than old turns."""
        recent_turn = self.create_test_turn("Recent question about AI", "user", 1.0)
        old_turn = self.create_test_turn("Old question about AI", "user", 48.0)
        
        scores = self.scorer.score_context_turns(
            [recent_turn, old_turn],
            "Tell me about AI",
            self.current_time
        )
        
        recent_score = next(s for s in scores if s.turn_id == recent_turn.id)
        old_score = next(s for s in scores if s.turn_id == old_turn.id)
        
        assert recent_score.recency_score > old_score.recency_score
    
    def test_relevance_scoring(self):
        """Test that relevant turns score higher than irrelevant turns."""
        relevant_turn = self.create_test_turn("How do I implement neural networks?", "user", 12.0)
        irrelevant_turn = self.create_test_turn("What's for lunch today?", "user", 12.0)
        
        scores = self.scorer.score_context_turns(
            [relevant_turn, irrelevant_turn],
            "Explain machine learning algorithms",
            self.current_time
        )
        
        relevant_score = next(s for s in scores if s.turn_id == relevant_turn.id)
        irrelevant_score = next(s for s in scores if s.turn_id == irrelevant_turn.id)
        
        assert relevant_score.relevance_score > irrelevant_score.relevance_score
    
    def test_combined_scoring(self):
        """Test that combined scoring balances recency and relevance."""
        # Recent but irrelevant
        recent_irrelevant = self.create_test_turn("Random question about cats", "user", 1.0)
        
        # Old but highly relevant  
        old_relevant = self.create_test_turn("How do I optimize neural network training?", "user", 24.0)
        
        scores = self.scorer.score_context_turns(
            [recent_irrelevant, old_relevant],
            "What are the best practices for training machine learning models?",
            self.current_time
        )
        
        # The old but relevant should win due to high relevance weight (0.7)
        assert scores[0].turn_id == old_relevant.id
    
    def test_optimal_context_selection(self):
        """Test context selection within token limits."""
        turns = [
            self.create_test_turn("Question about AI", "user", 1.0, tokens=20),
            self.create_test_turn("Answer about AI", "assistant", 1.0, tokens=100),
            self.create_test_turn("Question about cooking", "user", 2.0, tokens=15),
            self.create_test_turn("Question about machine learning", "user", 3.0, tokens=25),
        ]
        
        selected = self.scorer.get_optimal_context(
            turns,
            "Tell me more about artificial intelligence",
            max_tokens=150,  # Should select AI-related turns
            current_time=self.current_time
        )
        
        # Should prioritize AI-related content within token limit
        assert len(selected) > 0
        total_tokens = sum(turn.tokens for turn in selected)
        assert total_tokens <= 150
        
        # Should be in chronological order
        for i in range(1, len(selected)):
            assert selected[i].timestamp >= selected[i-1].timestamp
    
    def test_score_reasoning(self):
        """Test that scoring provides human-readable reasoning."""
        turn = self.create_test_turn("Recent relevant question", "user", 2.0)
        scores = self.scorer.score_context_turns(
            [turn],
            "Related query",
            self.current_time
        )
        
        assert len(scores) == 1
        assert isinstance(scores[0].reasoning, str)
        assert len(scores[0].reasoning) > 0


class TestAdvancedContextScorer:
    """Test enhanced context scoring features."""
    
    def setup_method(self):
        self.scorer = AdvancedContextScorer()
        self.current_time = datetime.now(timezone.utc)
    
    def create_test_turn(self, content: str, role: str, hours_ago: float) -> ConversationTurn:
        """Helper to create test conversation turns."""
        timestamp = self.current_time - timedelta(hours=hours_ago)
        return ConversationTurn(
            id=f"turn_{role}_{hours_ago}",
            content=content,
            role=role,
            timestamp=timestamp,
            tokens=50
        )
    
    def test_question_answer_pair_bonus(self):
        """Test that Q&A pairs get scoring bonuses."""
        # Create a question-answer pair
        question = self.create_test_turn("How does machine learning work?", "user", 2.0)
        answer = self.create_test_turn("Machine learning uses algorithms to find patterns...", "assistant", 2.0)
        isolated_question = self.create_test_turn("Random question?", "user", 2.0)
        
        turns = [question, answer, isolated_question]
        scores = self.scorer.score_context_turns(
            turns,
            "Explain AI algorithms",
            self.current_time
        )
        
        question_score = next(s for s in scores if s.turn_id == question.id)
        answer_score = next(s for s in scores if s.turn_id == answer.id)
        isolated_score = next(s for s in scores if s.turn_id == isolated_question.id)
        
        # Q&A pair should get bonuses
        assert "pair=" in question_score.reasoning
        assert "pair=" in answer_score.reasoning
        assert "pair=0.00" in isolated_score.reasoning
    
    def test_conversation_boundary_bonus(self):
        """Test that conversation boundaries get bonuses."""
        question_turn = self.create_test_turn("What is neural network?", "user", 1.0)
        statement_turn = self.create_test_turn("I think AI is interesting", "user", 1.0)
        
        turns = [question_turn, statement_turn]
        scores = self.scorer.score_context_turns(
            turns,
            "Tell me about AI",
            self.current_time
        )
        
        question_score = next(s for s in scores if s.turn_id == question_turn.id)
        statement_score = next(s for s in scores if s.turn_id == statement_turn.id)
        
        # Question should get boundary bonus
        assert "boundary=" in question_score.reasoning
        assert "boundary=" in statement_score.reasoning


class TestRealWorldScenarios:
    """Test with realistic conversation scenarios."""
    
    def setup_method(self):
        self.scorer = AdvancedContextScorer()
        self.current_time = datetime.now(timezone.utc)
    
    def test_programming_help_conversation(self):
        """Test scoring in a programming help context."""
        turns = [
            ConversationTurn("1", "How do I debug Python code?", "user", 
                           self.current_time - timedelta(hours=1), 20),
            ConversationTurn("2", "Use debugger and print statements...", "assistant",
                           self.current_time - timedelta(hours=1), 80),
            ConversationTurn("3", "What about JavaScript debugging?", "user",
                           self.current_time - timedelta(hours=0.5), 25),
            ConversationTurn("4", "Browser dev tools are great for...", "assistant",
                           self.current_time - timedelta(hours=0.5), 90),
            ConversationTurn("5", "How's the weather?", "user",
                           self.current_time - timedelta(minutes=30), 15),
        ]
        
        # Query about Python debugging should prioritize relevant turns
        selected = self.scorer.get_optimal_context(
            turns,
            "Show me Python debugging techniques",
            max_tokens=200,
            current_time=self.current_time
        )
        
        # Should include Python debugging Q&A pair
        selected_ids = {turn.id for turn in selected}
        assert "1" in selected_ids  # Python question
        assert "2" in selected_ids  # Python answer
        
        # Should exclude weather question due to irrelevance
        assert "5" not in selected_ids
    
    def test_long_conversation_context_management(self):
        """Test context selection in long conversations."""
        # Simulate 20 turns over 2 days
        turns = []
        for i in range(20):
            hours_ago = i * 2.4  # Spread over 48 hours
            content = f"Question {i} about topic {i % 3}"  # Rotating topics
            role = "user" if i % 2 == 0 else "assistant"
            
            turns.append(ConversationTurn(
                str(i),
                content,
                role,
                self.current_time - timedelta(hours=hours_ago),
                30
            ))
        
        # Recent query about topic 0
        selected = self.scorer.get_optimal_context(
            turns,
            "More about topic 0",
            max_tokens=300,
            current_time=self.current_time
        )
        
        # Should prioritize recent and relevant turns
        assert len(selected) > 0
        total_tokens = sum(turn.tokens for turn in selected)
        assert total_tokens <= 300
        
        # Should include some recent turns about topic 0
        topic_0_turns = [turn for turn in selected if "topic 0" in turn.content]
        assert len(topic_0_turns) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])