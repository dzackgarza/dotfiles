"""
Message definitions for V3 Textual app

These messages enable communication between widgets using Textual's message system.
"""

from textual.message import Message


class UserMessage(Message):
    """Message sent when user submits input"""
    
    def __init__(self, text: str):
        self.text = text
        super().__init__()


class ClearTimeline(Message):
    """Message to clear the timeline"""
    pass


class ProcessingComplete(Message):
    """Message sent when LLM processing completes"""
    
    def __init__(self, result: dict):
        self.result = result
        super().__init__()


class ProcessingError(Message):
    """Message sent when LLM processing fails"""
    
    def __init__(self, error: str):
        self.error = error
        super().__init__()


class StatusUpdate(Message):
    """Message to update status display"""
    
    def __init__(self, message: str, status_type: str = "ready"):
        self.message = message
        self.status_type = status_type  # "ready", "processing", "error"
        super().__init__()