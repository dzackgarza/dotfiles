"""
Input Panel Component

Modern input panel that replaces V2's basic input area
with a professional, feature-rich input component.
"""

import tkinter as tk
from typing import Callable, Optional
from .styles import ModernTheme


class InputPanel:
    """
    Modern input panel component.
    
    Builds on V2's working input functionality but with modern styling,
    better organization, and enhanced features.
    """
    
    def __init__(self, parent: tk.Widget, theme: ModernTheme = None):
        self.parent = parent
        self.theme = theme or ModernTheme()
        self.send_callback: Optional[Callable[[str], None]] = None
        self.clear_callback: Optional[Callable[[], None]] = None
        self.is_processing = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the input panel UI components."""
        # Main frame
        self.frame = tk.Frame(self.parent)
        self.theme.apply_to_widget(self.frame, 'input_frame')
        
        # Header
        self.header_label = tk.Label(
            self.frame,
            text="💬 Input (Multiline, Expanding)"
        )
        self.theme.apply_to_widget(self.header_label, 'label_heading')
        self.header_label.pack(anchor=tk.W, padx=self.theme.SPACING['md'], 
                              pady=(self.theme.SPACING['md'], self.theme.SPACING['sm']))
        
        # Input text area
        self.input_text = tk.Text(
            self.frame,
            width=100,
            height=5,
            wrap=tk.WORD
        )
        self.theme.apply_to_widget(self.input_text, 'input_text')
        self.input_text.pack(fill=tk.X, padx=self.theme.SPACING['md'], 
                            pady=(0, self.theme.SPACING['sm']))
        
        # Bind events for expanding input and keyboard shortcuts
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Control-Return>', self.on_ctrl_enter)
        self.input_text.bind('<Shift-Return>', self.on_shift_enter)
        
        # Button and status frame
        self.button_frame = tk.Frame(self.frame)
        self.theme.apply_to_widget(self.button_frame, 'input_frame')
        self.button_frame.pack(fill=tk.X, padx=self.theme.SPACING['md'], 
                              pady=(0, self.theme.SPACING['md']))
        
        # Send button
        self.send_button = tk.Button(
            self.button_frame,
            text="Send (Enter)",
            command=self.send_message
        )
        self.theme.apply_to_widget(self.send_button, 'button_primary')
        self.theme.configure_button_hover(self.send_button, 'button_primary')
        self.send_button.pack(side=tk.LEFT, padx=(0, self.theme.SPACING['sm']))
        
        # Clear button
        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear Timeline",
            command=self.clear_timeline
        )
        self.theme.apply_to_widget(self.clear_button, 'button_secondary')
        self.theme.configure_button_hover(self.clear_button, 'button_secondary')
        self.clear_button.pack(side=tk.LEFT, padx=(0, self.theme.SPACING['md']))
        
        # Character count label
        self.char_count_label = tk.Label(
            self.button_frame,
            text="0 characters"
        )
        self.theme.apply_to_widget(self.char_count_label, 'label_body')
        self.char_count_label.pack(side=tk.LEFT, padx=(self.theme.SPACING['md'], 0))
        
        # Status label
        self.status_label = tk.Label(
            self.button_frame,
            text="Ready"
        )
        self.theme.apply_to_widget(self.status_label, 'status_ready')
        self.status_label.pack(side=tk.RIGHT)
        
        # Focus input
        self.input_text.focus_set()
    
    def on_input_change(self, event):
        """Handle input text changes for expanding and character count."""
        # Get current content
        content = self.input_text.get("1.0", tk.END)
        
        # Update character count
        char_count = len(content.strip())
        self.char_count_label.config(text=f"{char_count} characters")
        
        # Adjust height based on content (min 3, max 10 lines)
        lines = content.count('\\n')
        new_height = max(3, min(10, lines + 2))
        self.input_text.config(height=new_height)
    
    def on_enter_key(self, event):
        """Handle Enter key - send message unless Shift is held."""
        if event.state & 0x1:  # Shift key held
            return  # Allow newline
        else:
            self.send_message()
            return "break"  # Prevent default newline
    
    def on_ctrl_enter(self, event):
        """Handle Ctrl+Enter - force send."""
        self.send_message()
        return "break"
    
    def on_shift_enter(self, event):
        """Handle Shift+Enter - allow newline."""
        return  # Allow default newline behavior
    
    def send_message(self):
        """Send the current message."""
        if self.is_processing:
            return
        
        # Get input text
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return
        
        # Clear input and reset height
        self.input_text.delete("1.0", tk.END)
        self.input_text.config(height=3)
        self.char_count_label.config(text="0 characters")
        
        # Call send callback if set
        if self.send_callback:
            self.send_callback(user_input)
    
    def clear_timeline(self):
        """Clear the timeline."""
        if self.clear_callback:
            self.clear_callback()
    
    def set_send_callback(self, callback: Callable[[str], None]):
        """Set the callback for when a message is sent."""
        self.send_callback = callback
    
    def set_clear_callback(self, callback: Callable[[], None]):
        """Set the callback for when timeline is cleared."""
        self.clear_callback = callback
    
    def set_processing_state(self, processing: bool):
        """Set the processing state."""
        self.is_processing = processing
        
        if processing:
            self.send_button.config(state=tk.DISABLED)
            self.input_text.config(state=tk.DISABLED)
        else:
            self.send_button.config(state=tk.NORMAL)
            self.input_text.config(state=tk.NORMAL)
            self.input_text.focus_set()
    
    def update_status(self, message: str, status_type: str = "ready"):
        """Update the status label."""
        self.status_label.config(text=message)
        
        # Apply appropriate style based on status type
        if status_type == "processing":
            self.theme.apply_to_widget(self.status_label, 'status_processing')
        elif status_type == "error":
            self.theme.apply_to_widget(self.status_label, 'status_error')
        else:  # ready
            self.theme.apply_to_widget(self.status_label, 'status_ready')
    
    def pack(self, **kwargs):
        """Pack the input panel."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the input panel."""
        self.frame.grid(**kwargs)
    
    def get_current_input(self) -> str:
        """Get the current input text."""
        return self.input_text.get("1.0", tk.END).strip()
    
    def set_input_text(self, text: str):
        """Set the input text programmatically."""
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", text)
        self.on_input_change(None)  # Update character count and height
    
    def focus_input(self):
        """Focus the input text area."""
        self.input_text.focus_set()
    
    def add_placeholder_text(self, placeholder: str):
        """Add placeholder text functionality."""
        def on_focus_in(event):
            if self.input_text.get("1.0", tk.END).strip() == placeholder:
                self.input_text.delete("1.0", tk.END)
                self.input_text.config(fg=self.theme.COLORS['text_primary'])
        
        def on_focus_out(event):
            if not self.input_text.get("1.0", tk.END).strip():
                self.input_text.insert("1.0", placeholder)
                self.input_text.config(fg=self.theme.COLORS['text_muted'])
        
        # Set initial placeholder
        self.input_text.insert("1.0", placeholder)
        self.input_text.config(fg=self.theme.COLORS['text_muted'])
        
        # Bind events
        self.input_text.bind('<FocusIn>', on_focus_in)
        self.input_text.bind('<FocusOut>', on_focus_out)