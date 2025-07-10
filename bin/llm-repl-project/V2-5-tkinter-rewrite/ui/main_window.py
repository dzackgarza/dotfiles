"""
Main Window - Modern Application Window

Replaces V2's basic tkinter window with a modern, professional interface
while preserving all the working functionality.
"""

import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
from typing import Optional
from core import TimelineManager, CognitionProcessor, create_user_input_block, create_cognition_block, create_assistant_response_block, create_error_block
from .timeline_view import TimelineView
from .input_panel import InputPanel
from .styles import ModernTheme, DarkTheme


class MainWindow:
    """
    Modern main application window.
    
    Builds on V2's working functionality but with a modern, professional
    interface and better organization.
    """
    
    def __init__(self, config_name: str = "debug", theme_name: str = "light"):
        self.config_name = config_name
        self.theme = DarkTheme() if theme_name == "dark" else ModernTheme()
        
        # Core components (extracted from V2)
        self.timeline_manager = TimelineManager()
        self.cognition_processor = CognitionProcessor()
        
        # UI components
        self.root: Optional[tk.Tk] = None
        self.timeline_view: Optional[TimelineView] = None
        self.input_panel: Optional[InputPanel] = None
        
        # State
        self.is_processing = False
        
        # Setup
        self.setup_window()
        self.setup_components()
        self.setup_callbacks()
        self.initialize_timeline()
    
    def setup_window(self):
        """Setup the main window."""
        self.root = tk.Tk()
        self.root.title(f"LLM REPL V3 - Modern Interface (Config: {self.config_name})")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Apply theme to root window
        self.theme.apply_to_widget(self.root, 'window')
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def setup_components(self):
        """Setup the UI components."""
        # Main container
        main_frame = tk.Frame(self.root)
        self.theme.apply_to_widget(main_frame, 'main_frame')
        main_frame.pack(fill=tk.BOTH, expand=True, 
                       padx=self.theme.SPACING['md'], 
                       pady=self.theme.SPACING['md'])
        
        # Timeline view (top 70%)
        self.timeline_view = TimelineView(main_frame, self.theme)
        self.timeline_view.pack(fill=tk.BOTH, expand=True, 
                               pady=(0, self.theme.SPACING['md']))
        
        # Input panel (bottom 30%)
        self.input_panel = InputPanel(main_frame, self.theme)
        self.input_panel.pack(fill=tk.X)
        
        # Setup menu bar
        self.setup_menu_bar()
    
    def setup_menu_bar(self):
        """Setup the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Timeline...", command=self.export_timeline)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_window_close)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Increase Font Size", command=lambda: self.change_font_size(1))
        view_menu.add_command(label="Decrease Font Size", command=lambda: self.change_font_size(-1))
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
    
    def setup_callbacks(self):
        """Setup callbacks between components."""
        # Connect input panel to message processing
        self.input_panel.set_send_callback(self.on_send_message)
        self.input_panel.set_clear_callback(self.on_clear_timeline)
        
        # Connect timeline manager to timeline view
        self.timeline_manager.add_observer(self.on_timeline_block_added)
    
    def initialize_timeline(self):
        """Initialize the timeline with startup blocks."""
        self.timeline_manager.initialize_with_startup_blocks(self.config_name)
    
    def on_timeline_block_added(self, block):
        """Handle when a block is added to the timeline."""
        if self.timeline_view:
            self.timeline_view.add_block(block)
    
    def on_send_message(self, user_input: str):
        """Handle when a message is sent."""
        if self.is_processing:
            return
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit']:
            self.on_window_close()
            return
        
        # Process message in background thread
        threading.Thread(
            target=self.process_message_async, 
            args=(user_input,), 
            daemon=True
        ).start()
    
    def on_clear_timeline(self):
        """Handle timeline clear request."""
        if messagebox.askyesno(
            "Clear Timeline", 
            "Are you sure you want to clear the timeline?\\n\\nThis will remove all conversation history.",
            parent=self.root
        ):
            self.timeline_view.clear()
            self.timeline_manager.clear_timeline()
            self.timeline_manager.initialize_with_startup_blocks(self.config_name)
            self.input_panel.update_status("Timeline cleared", "ready")
    
    def process_message_async(self, user_input: str):
        """Process message asynchronously (extracted from V2)."""
        # Run async processing in thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.process_message(user_input))
        finally:
            loop.close()
    
    async def process_message(self, user_input: str):
        """Process user message through the block pipeline (from V2)."""
        self.is_processing = True
        
        # Update UI state
        self.root.after(0, lambda: self.input_panel.set_processing_state(True))
        
        try:
            # 1. User Input Block
            self.root.after(0, lambda: self.input_panel.update_status(
                "Processing user input...", "processing"))
            
            user_block = create_user_input_block(user_input)
            self.root.after(0, lambda: self.timeline_manager.add_block(user_block))
            
            # 2. Cognition Block
            self.root.after(0, lambda: self.input_panel.update_status(
                "Processing through cognition...", "processing"))
            
            cognition_result = await self.cognition_processor.process(user_input)
            
            cognition_block = create_cognition_block(
                cognition_result["transparency_log"],
                cognition_result["total_tokens"],
                cognition_result["processing_duration"]
            )
            self.root.after(0, lambda: self.timeline_manager.add_block(cognition_block))
            
            # 3. Assistant Response Block
            self.root.after(0, lambda: self.input_panel.update_status(
                "Generating response...", "processing"))
            
            assistant_block = create_assistant_response_block(
                cognition_result["final_output"],
                cognition_result["total_tokens"],
                cognition_result
            )
            self.root.after(0, lambda: self.timeline_manager.add_block(assistant_block))
            
            # Update status
            self.root.after(0, lambda: self.input_panel.update_status("Ready", "ready"))
            
        except Exception as e:
            # Error block
            error_block = create_error_block(str(e))
            self.root.after(0, lambda: self.timeline_manager.add_block(error_block))
            self.root.after(0, lambda: self.input_panel.update_status(
                "Error occurred", "error"))
        
        finally:
            self.is_processing = False
            # Re-enable UI
            self.root.after(0, lambda: self.input_panel.set_processing_state(False))
    
    def export_timeline(self):
        """Export timeline to a file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Export Timeline",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            parent=self.root
        )
        
        if filename:
            try:
                timeline_text = self.timeline_manager.get_timeline_text()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(timeline_text)
                messagebox.showinfo(
                    "Export Successful", 
                    f"Timeline exported to {filename}",
                    parent=self.root
                )
            except Exception as e:
                messagebox.showerror(
                    "Export Failed", 
                    f"Failed to export timeline: {str(e)}",
                    parent=self.root
                )
    
    def change_font_size(self, delta: int):
        """Change the font size for accessibility."""
        current_size = self.theme.FONTS['code'][1]
        new_size = max(8, min(20, current_size + delta))
        
        if self.timeline_view:
            self.timeline_view.set_font_size(new_size)
        
        # Update theme font size
        self.theme.FONTS = {
            **self.theme.FONTS,
            'code': (self.theme.FONTS['code'][0], new_size)
        }
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        # This would require recreating the UI with the new theme
        # For now, just show a message
        messagebox.showinfo(
            "Theme Toggle", 
            "Theme switching will be available in a future update.\\n\\n"
            "Restart the application with --theme dark for dark mode.",
            parent=self.root
        )
    
    def show_about(self):
        """Show about dialog."""
        about_text = f"""LLM REPL V3 - Modern Interface

Version: 3.0.0
Configuration: {self.config_name}
Theme: {"Dark" if isinstance(self.theme, DarkTheme) else "Light"}

A modern, professional interface for LLM interactions
with block-based timeline and cognitive processing.

Built on the reliable foundation of V2 with
modern styling and enhanced user experience."""
        
        messagebox.showinfo("About LLM REPL V3", about_text, parent=self.root)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        shortcuts_text = """Keyboard Shortcuts:

• Enter: Send message
• Shift+Enter: New line in input
• Ctrl+Enter: Force send message
• Ctrl+Q: Quit application
• Ctrl+L: Clear timeline
• Ctrl++: Increase font size
• Ctrl+-: Decrease font size

Input Commands:
• 'exit' or 'quit': Close application"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text, parent=self.root)
    
    def on_window_close(self):
        """Handle window close event."""
        if self.is_processing:
            if not messagebox.askyesno(
                "Processing in Progress", 
                "A message is currently being processed.\\n\\n"
                "Are you sure you want to exit?",
                parent=self.root
            ):
                return
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        print("🚀 Starting LLM REPL V3 - Modern Interface...")
        print(f"📋 Configuration: {self.config_name}")
        print(f"🎨 Theme: {'Dark' if isinstance(self.theme, DarkTheme) else 'Light'}")
        print("🎯 Features: Modern UI, block-based timeline, cognitive processing")
        print("💡 GUI will open in a new window...")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n👋 Goodbye!")
        finally:
            try:
                if self.root:
                    self.root.destroy()
            except:
                pass