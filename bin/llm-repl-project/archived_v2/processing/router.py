"""Query routing to appropriate handlers based on intent."""

from typing import Any, Dict, Optional, Callable, Awaitable
from dataclasses import dataclass

from .intent import QueryIntent, IntentDetector


@dataclass
class RoutingResult:
    """Result of query routing."""
    intent: QueryIntent
    handler_name: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class QueryRouter:
    """Routes queries to appropriate handlers based on detected intent."""
    
    def __init__(self, intent_detector: IntentDetector):
        """
        Initialize the query router.
        
        Args:
            intent_detector: The intent detector to use
        """
        self.intent_detector = intent_detector
        self.handlers: Dict[QueryIntent, Callable[[str], Awaitable[Any]]] = {}
        self.handler_names: Dict[QueryIntent, str] = {
            QueryIntent.CHAT: "Chat Agent",
            QueryIntent.SEARCH: "Literature Search Agent",
            QueryIntent.COMPUTE: "Math Agent",
            QueryIntent.CODE: "Code Agent", 
            QueryIntent.SYNTHESIZE: "Synthesis Agent"
        }
    
    def register_handler(self, intent: QueryIntent, handler: Callable[[str], Awaitable[Any]], 
                        name: Optional[str] = None) -> None:
        """
        Register a handler for a specific intent.
        
        Args:
            intent: The intent to handle
            handler: The async handler function
            name: Optional custom name for the handler
        """
        self.handlers[intent] = handler
        if name:
            self.handler_names[intent] = name
    
    async def route_query(self, query: str) -> RoutingResult:
        """
        Route a query to the appropriate handler.
        
        Args:
            query: The user's input query
            
        Returns:
            RoutingResult with intent and handler information
        """
        # Detect intent
        intent = await self.intent_detector.detect_intent(query)
        
        # Get handler name
        handler_name = self.handler_names.get(intent, "Unknown Handler")
        
        # Create routing result
        result = RoutingResult(
            intent=intent,
            handler_name=handler_name,
            metadata={
                "query": query,
                "has_handler": intent in self.handlers
            }
        )
        
        return result
    
    async def execute_query(self, query: str) -> Any:
        """
        Route and execute a query with the appropriate handler.
        
        Args:
            query: The user's input query
            
        Returns:
            The result from the handler
            
        Raises:
            ValueError: If no handler is registered for the detected intent
        """
        routing_result = await self.route_query(query)
        
        if routing_result.intent not in self.handlers:
            raise ValueError(f"No handler registered for intent: {routing_result.intent}")
        
        handler = self.handlers[routing_result.intent]
        return await handler(query)
    
    def get_routing_info(self) -> Dict[str, Any]:
        """Get information about current routing configuration."""
        return {
            "registered_handlers": {
                intent.value: {
                    "name": self.handler_names.get(intent),
                    "registered": intent in self.handlers
                }
                for intent in QueryIntent
            }
        }