"""
Timeline View Component

Modern timeline display that replaces V2's basic text widget
with a professional, styled timeline view.
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Optional
from core.blocks import TimelineBlock
from .styles import ModernTheme


class TimelineView:
    """
    Modern timeline view component.
    
    Builds on V2's working timeline display but with modern styling
    and better organization.
    """
    
    def __init__(self, parent: tk.Widget, theme: ModernTheme = None):
        self.parent = parent
        self.theme = theme or ModernTheme()
        self.setup_ui()
        self.configure_text_tags()
    
    def setup_ui(self):
        """Setup the timeline UI components."""
        # Main frame
        self.frame = tk.Frame(self.parent)
        self.theme.apply_to_widget(self.frame, 'timeline_frame')
        
        # Header
        self.header_label = tk.Label(
            self.frame,
            text="📜 Timeline (Live/Inscribed Blocks)"
        )
        self.theme.apply_to_widget(self.header_label, 'label_heading')
        self.header_label.pack(anchor=tk.W, padx=self.theme.SPACING['md'], 
                              pady=(self.theme.SPACING['md'], self.theme.SPACING['sm']))
        
        # Timeline text widget
        self.text_widget = scrolledtext.ScrolledText(
            self.frame,
            state=tk.DISABLED,
            width=100,
            height=25
        )
        self.theme.apply_to_widget(self.text_widget, 'timeline_text')
        self.text_widget.pack(fill=tk.BOTH, expand=True, 
                             padx=self.theme.SPACING['md'], 
                             pady=(0, self.theme.SPACING['md']))
    
    def configure_text_tags(self):
        """Configure text tags for styling different parts of the timeline."""
        # Block header tag
        self.text_widget.tag_configure(
            "block_header",
            font=self.theme.FONTS['subheading'],
            foreground=self.theme.COLORS['text_primary'],
            spacing1=self.theme.SPACING['sm'],
            spacing3=self.theme.SPACING['xs']
        )
        
        # Block content tag
        self.text_widget.tag_configure(
            "block_content",
            font=self.theme.FONTS['code'],
            foreground=self.theme.COLORS['text_secondary'],
            lmargin1=self.theme.SPACING['md'],
            lmargin2=self.theme.SPACING['md']
        )
        
        # Block type specific tags
        block_types = ['system_check', 'welcome', 'user_input', 'cognition', 'assistant_response', 'error']
        for block_type in block_types:
            self.text_widget.tag_configure(
                f"header_{block_type}",
                foreground=self.theme.get_block_color(block_type),
                font=self.theme.FONTS['subheading']
            )
        
        # Separator tag
        self.text_widget.tag_configure(
            "separator",
            foreground=self.theme.COLORS['border'],
            justify=tk.CENTER,
            spacing1=self.theme.SPACING['sm'],
            spacing3=self.theme.SPACING['sm']
        )
    
    def add_block(self, block: TimelineBlock):
        """Add a block to the timeline display."""
        self.text_widget.config(state=tk.NORMAL)
        
        # Add separator if not first block
        if self.text_widget.get("1.0", tk.END).strip():
            separator = "─" * 80 + "\\n\\n"
            self.text_widget.insert(tk.END, separator, "separator")
        
        # Add block header with type-specific styling
        header = block.get_formatted_header() + "\\n"
        header_tag = f"header_{block.type.value}"
        self.text_widget.insert(tk.END, header, header_tag)
        
        # Add block content
        content = block.content + "\\n"
        self.text_widget.insert(tk.END, content, "block_content")
        
        self.text_widget.config(state=tk.DISABLED)
        
        # Auto-scroll to bottom
        self.text_widget.see(tk.END)
    
    def clear(self):
        """Clear the timeline display."""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def pack(self, **kwargs):
        """Pack the timeline view."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the timeline view."""
        self.frame.grid(**kwargs)
    
    def get_text_content(self) -> str:
        """Get the current text content of the timeline."""
        return self.text_widget.get("1.0", tk.END)
    
    def export_as_text(self) -> str:
        """Export timeline as plain text."""
        return self.get_text_content().strip()
    
    def set_font_size(self, size: int):
        """Adjust font size for accessibility."""
        new_font = (self.theme.FONTS['code'][0], size)
        self.text_widget.configure(font=new_font)
        
        # Update tag fonts
        self.text_widget.tag_configure("block_content", font=new_font)
        
        header_font = (self.theme.FONTS['subheading'][0], size + 2, 'bold')
        self.text_widget.tag_configure("block_header", font=header_font)
        
        for block_type in ['system_check', 'welcome', 'user_input', 'cognition', 'assistant_response', 'error']:
            self.text_widget.tag_configure(f"header_{block_type}", font=header_font)