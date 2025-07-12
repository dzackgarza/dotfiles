"""Reality command provider for visual verification"""

from textual.command import Command, Hit, Hits, Provider


class RealityCommandProvider(Provider):
    """Reality check commands for visual verification"""

    async def search(self, query: str) -> Hits:
        """Search for reality check commands"""
        
        def make_hit(name: str, description: str, command_name: str) -> Hit:
            """Create a command hit"""
            def run_command() -> None:
                self.app.action_reality_command(command_name)
            
            return Hit(
                score=1.0,
                match_display=name,
                command=run_command,
            )

        commands = [
            ("Take Reality Screenshot", "Take screenshot to verify GUI state", "screenshot"),
            ("Visual State Check", "Check what's actually visible", "visual_check"),
            ("Layout Reality", "Verify layout matches expectations", "layout_check"),
            ("Content Audit", "Count and verify visible content", "content_audit"),
            ("Scroll State", "Check scroll position and range", "scroll_state"),
        ]

        matcher = self.matcher(query)
        
        for name, description, command_name in commands:
            if not query or matcher.match(name):
                yield make_hit(name, description, command_name)


def action_reality_command(self, command: str) -> None:
    """Handle reality check commands - to be added to LLMReplApp"""
    if command == "screenshot":
        filename = self.create_debug_screenshot("reality_check")
        self.notify(f"Reality screenshot saved: {filename}")
        
    elif command == "visual_check":
        try:
            container = self.chat_container
            children_count = len(container.children)
            scroll_info = f"{container.scroll_y:.1f}/{container.max_scroll_y}"
            self.notify(f"Visual: {children_count} items, scroll {scroll_info}")
        except Exception as e:
            self.notify(f"Visual check error: {e}")
            
    elif command == "layout_check":
        try:
            main_size = self.size
            container_size = self.chat_container.size
            self.notify(f"Layout: App {main_size}, Container {container_size}")
        except Exception as e:
            self.notify(f"Layout check error: {e}")
            
    elif command == "content_audit":
        try:
            container = self.chat_container
            widget_types = {}
            for child in container.children:
                widget_type = child.__class__.__name__
                widget_types[widget_type] = widget_types.get(widget_type, 0) + 1
            
            audit_text = ", ".join([f"{k}: {v}" for k, v in widget_types.items()])
            self.notify(f"Content: {audit_text}")
        except Exception as e:
            self.notify(f"Content audit error: {e}")
            
    elif command == "scroll_state":
        try:
            container = self.chat_container
            current = container.scroll_y
            maximum = container.max_scroll_y
            height = container.size.height
            virtual = container.virtual_size.height
            self.notify(f"Scroll: {current:.1f}/{maximum}, h:{height}, vh:{virtual}")
        except Exception as e:
            self.notify(f"Scroll state error: {e}")
            
    else:
        self.notify(f"Unknown reality command: {command}")
