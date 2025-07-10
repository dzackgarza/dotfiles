"""System blocks for application lifecycle."""

from typing import Dict, Any, List
from .base import Block, BlockType


class SystemCheckBlock(Block):
    """System check block displayed at startup."""
    
    def __init__(self):
        super().__init__(BlockType.SYSTEM_CHECK, "System Check")
        self.checks: List[Dict[str, Any]] = []
        self.all_passed = False
    
    def add_check(self, name: str, passed: bool, message: str) -> None:
        """Add a check result."""
        self.checks.append({
            "name": name,
            "passed": passed,
            "message": message
        })
    
    def _on_start(self) -> None:
        """Start system checks."""
        self.content.metadata["status"] = "checking"
    
    def _on_complete(self) -> None:
        """Complete system checks."""
        self.all_passed = all(check["passed"] for check in self.checks)
        self.content.metadata["status"] = "complete"
        self.content.metadata["result"] = "passed" if self.all_passed else "failed"
    
    def render_live(self) -> Dict[str, Any]:
        """Render system check in progress."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": "🔍 System Check",
            "body": "Checking system components...",
            "style": "system_check",
            "show_spinner": True,
            "checks": self.checks
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Render completed system check."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": "✅ System Check" if self.all_passed else "❌ System Check Failed",
            "style": "system_check_complete",
            "checks": self.checks,
            "all_passed": self.all_passed
        }


class WelcomeBlock(Block):
    """Welcome message block."""
    
    def __init__(self, version: str = "v2"):
        welcome_text = f"Welcome to LLM REPL {version}! Type your queries below."
        super().__init__(BlockType.WELCOME, f"🚀 LLM REPL {version}", welcome_text)
        self.version = version
    
    def _on_start(self) -> None:
        """Welcome blocks display immediately."""
        pass
    
    def _on_complete(self) -> None:
        """Welcome blocks complete immediately."""
        pass
    
    def render_live(self) -> Dict[str, Any]:
        """Render welcome message."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.content.body,
            "style": "welcome",
            "box_style": "heavy"
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Welcome message doesn't change when inscribed."""
        return self.render_live()