"""
V3 Chatbox Copy - Simple chat message widget
Directly copied from V3's proven Chatbox pattern for perfect sizing
"""

from rich.console import RenderableType
from rich.markdown import Markdown
from textual.widget import Widget


class Chatbox(Widget, can_focus=True):
    """Direct copy of V3's Chatbox widget pattern"""

    def __init__(self, message_content: str, role: str = "user", **kwargs):
        super().__init__(**kwargs)
        self.content = message_content
        self.role = role

        # Set border title based on role
        role_titles = {
            "user": "> User",
            "assistant": "> Assistant",
            "cognition": "> Cognition",
            "system": "> System",
        }
        self.border_title = role_titles.get(role, "> Unknown")

        # V3's exact CSS classes
        self.add_class("chatbox")
        if role == "user":
            self.add_class("human-message")
        elif role == "assistant":
            self.add_class("assistant-message")
        elif role == "system":
            self.add_class("system-message")
        elif role == "cognition":
            self.add_class("cognition-message")

    def render(self) -> RenderableType:
        """V3's exact render pattern - role shown in border title"""
        # Simple markdown rendering like V3 (role prefix now in CSS border-title)
        return Markdown(self.content, code_theme="monokai")
