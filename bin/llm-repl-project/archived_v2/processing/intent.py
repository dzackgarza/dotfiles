"""Intent detection for query routing."""

from enum import Enum
from typing import Optional, List, Dict, Any
import asyncio


class QueryIntent(Enum):
    """Possible query intents."""
    CHAT = "CHAT"
    SEARCH = "SEARCH"
    COMPUTE = "COMPUTE"
    CODE = "CODE"
    SYNTHESIZE = "SYNTHESIZE"


class IntentDetector:
    """Detects user query intent for routing to appropriate handlers."""
    
    # Keywords for rule-based intent detection
    INTENT_KEYWORDS = {
        QueryIntent.SEARCH: ["search", "find", "research", "literature", "papers", "articles", "studies"],
        QueryIntent.COMPUTE: ["calculate", "math", "compute", "solve", "equation", "formula", "sum", "multiply"],
        QueryIntent.CODE: ["code", "program", "script", "function", "implement", "debug", "error", "syntax"],
        QueryIntent.SYNTHESIZE: ["analyze", "synthesis", "combine", "compare", "summarize", "explain", "contrast"]
    }
    
    def __init__(self, llm_manager: Optional[Any] = None):
        """
        Initialize the intent detector.
        
        Args:
            llm_manager: Optional LLM manager for AI-based intent detection
        """
        self.llm_manager = llm_manager
    
    async def detect_intent(self, query: str) -> QueryIntent:
        """
        Detect the intent of a user query using a 3-layer approach:
        1. Rule-based detection (fastest)
        2. AI-based detection (if rules don't match and LLM available)
        3. Default fallback (CHAT)
        
        Args:
            query: The user's input query
            
        Returns:
            The detected QueryIntent
        """
        # Layer 1: Rule-based detection
        intent = self._rule_based_detection(query)
        if intent != QueryIntent.CHAT:
            return intent
        
        # Layer 2: AI-based detection (if LLM manager available)
        if self.llm_manager:
            try:
                intent = await self._ai_based_detection(query)
                if intent != QueryIntent.CHAT:
                    return intent
            except Exception:
                # If AI detection fails, fall through to default
                pass
        
        # Layer 3: Default fallback
        return QueryIntent.CHAT
    
    def _rule_based_detection(self, query: str) -> QueryIntent:
        """
        Detect intent using keyword matching rules.
        
        Args:
            query: The user's input query
            
        Returns:
            The detected QueryIntent or CHAT if no rules match
        """
        query_lower = query.lower()
        
        # Check each intent's keywords
        for intent, keywords in self.INTENT_KEYWORDS.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return QueryIntent.CHAT
    
    async def _ai_based_detection(self, query: str) -> QueryIntent:
        """
        Detect intent using AI/LLM analysis.
        
        Args:
            query: The user's input query
            
        Returns:
            The detected QueryIntent
        """
        if not self.llm_manager:
            return QueryIntent.CHAT
        
        prompt = f"""Classify the following query into one of these categories:
- SEARCH: Looking for information, research papers, or literature
- COMPUTE: Mathematical calculations or problem solving
- CODE: Programming, debugging, or code-related questions
- SYNTHESIZE: Analysis, comparison, or synthesis of information
- CHAT: General conversation or questions

Query: "{query}"

Respond with only the category name."""

        try:
            response = await self.llm_manager.make_request(prompt, {"temperature": 0.1, "max_tokens": 10})
            intent_str = response.content.strip().upper()
            
            # Try to match the response to an intent
            for intent in QueryIntent:
                if intent.value == intent_str:
                    return intent
            
        except Exception:
            # If AI detection fails, return CHAT
            pass
        
        return QueryIntent.CHAT
    
    def get_intent_info(self, intent: QueryIntent) -> Dict[str, Any]:
        """
        Get information about a specific intent.
        
        Args:
            intent: The query intent
            
        Returns:
            Dictionary with intent information
        """
        return {
            "intent": intent.value,
            "description": self._get_intent_description(intent),
            "keywords": self.INTENT_KEYWORDS.get(intent, [])
        }
    
    def _get_intent_description(self, intent: QueryIntent) -> str:
        """Get a human-readable description of the intent."""
        descriptions = {
            QueryIntent.CHAT: "General conversation and questions",
            QueryIntent.SEARCH: "Information search and research",
            QueryIntent.COMPUTE: "Mathematical calculations",
            QueryIntent.CODE: "Programming and code assistance",
            QueryIntent.SYNTHESIZE: "Analysis and synthesis of information"
        }
        return descriptions.get(intent, "Unknown intent")