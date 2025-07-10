"""
Modern UI Styles and Themes

Replaces V2's 1995-style appearance with modern, professional styling.
"""

import tkinter as tk
from typing import Dict, Any


class ModernTheme:
    """
    Modern theme with professional colors and typography.
    
    This replaces V2's basic styling with a clean, modern appearance.
    """
    
    # Color palette - Modern, accessible colors
    COLORS = {
        # Primary colors
        'primary': '#2563eb',      # Blue
        'primary_hover': '#1d4ed8',
        'primary_light': '#dbeafe',
        
        # Secondary colors
        'secondary': '#64748b',    # Slate
        'secondary_hover': '#475569',
        'secondary_light': '#f1f5f9',
        
        # Success/Error colors
        'success': '#059669',      # Green
        'success_light': '#d1fae5',
        'warning': '#d97706',      # Orange
        'warning_light': '#fed7aa',
        'error': '#dc2626',        # Red
        'error_light': '#fee2e2',
        
        # Neutral colors
        'background': '#ffffff',
        'surface': '#f8fafc',
        'surface_hover': '#f1f5f9',
        'border': '#e2e8f0',
        'border_focus': '#3b82f6',
        
        # Text colors
        'text_primary': '#0f172a',
        'text_secondary': '#475569',
        'text_muted': '#94a3b8',
        'text_inverse': '#ffffff',
        
        # Block-specific colors
        'block_system': '#8b5cf6',     # Purple
        'block_welcome': '#06b6d4',    # Cyan
        'block_user': '#059669',       # Green
        'block_cognition': '#7c3aed',  # Violet
        'block_assistant': '#2563eb',  # Blue
        'block_error': '#dc2626',      # Red
    }
    
    # Typography
    FONTS = {
        'heading': ('Segoe UI', 14, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'code': ('Consolas', 10),
        'small': ('Segoe UI', 9),
    }
    
    # Spacing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
    }
    
    # Component styles
    STYLES = {
        'window': {
            'bg': COLORS['background'],
        },
        'main_frame': {
            'bg': COLORS['background'],
            'relief': tk.FLAT,
        },
        'timeline_frame': {
            'bg': COLORS['surface'],
            'relief': tk.FLAT,
            'bd': 1,
            'highlightbackground': COLORS['border'],
        },
        'timeline_text': {
            'bg': COLORS['background'],
            'fg': COLORS['text_primary'],
            'font': FONTS['code'],
            'relief': tk.FLAT,
            'bd': 0,
            'selectbackground': COLORS['primary_light'],
            'selectforeground': COLORS['text_primary'],
            'wrap': tk.WORD,
            'padx': SPACING['md'],
            'pady': SPACING['md'],
        },
        'input_frame': {
            'bg': COLORS['background'],
            'relief': tk.FLAT,
        },
        'input_text': {
            'bg': COLORS['background'],
            'fg': COLORS['text_primary'],
            'font': FONTS['body'],
            'relief': tk.SOLID,
            'bd': 1,
            'highlightbackground': COLORS['border'],
            'highlightcolor': COLORS['border_focus'],
            'highlightthickness': 1,
            'selectbackground': COLORS['primary_light'],
            'selectforeground': COLORS['text_primary'],
            'wrap': tk.WORD,
            'padx': SPACING['sm'],
            'pady': SPACING['sm'],
        },
        'button_primary': {
            'bg': COLORS['primary'],
            'fg': COLORS['text_inverse'],
            'font': FONTS['body'],
            'relief': tk.FLAT,
            'bd': 0,
            'padx': SPACING['md'],
            'pady': SPACING['sm'],
            'cursor': 'hand2',
        },
        'button_secondary': {
            'bg': COLORS['secondary'],
            'fg': COLORS['text_inverse'],
            'font': FONTS['body'],
            'relief': tk.FLAT,
            'bd': 0,
            'padx': SPACING['md'],
            'pady': SPACING['sm'],
            'cursor': 'hand2',
        },
        'label_heading': {
            'bg': COLORS['background'],
            'fg': COLORS['text_primary'],
            'font': FONTS['heading'],
        },
        'label_body': {
            'bg': COLORS['background'],
            'fg': COLORS['text_secondary'],
            'font': FONTS['body'],
        },
        'status_ready': {
            'bg': COLORS['background'],
            'fg': COLORS['success'],
            'font': FONTS['body'],
        },
        'status_processing': {
            'bg': COLORS['background'],
            'fg': COLORS['primary'],
            'font': FONTS['body'],
        },
        'status_error': {
            'bg': COLORS['background'],
            'fg': COLORS['error'],
            'font': FONTS['body'],
        },
    }
    
    @classmethod
    def apply_to_widget(cls, widget: tk.Widget, style_name: str):
        """Apply a style to a widget."""
        if style_name in cls.STYLES:
            widget.configure(**cls.STYLES[style_name])
    
    @classmethod
    def get_block_color(cls, block_type: str) -> str:
        """Get color for a specific block type."""
        color_map = {
            'system_check': cls.COLORS['block_system'],
            'welcome': cls.COLORS['block_welcome'],
            'user_input': cls.COLORS['block_user'],
            'cognition': cls.COLORS['block_cognition'],
            'assistant_response': cls.COLORS['block_assistant'],
            'error': cls.COLORS['block_error'],
        }
        return color_map.get(block_type, cls.COLORS['text_secondary'])
    
    @classmethod
    def configure_button_hover(cls, button: tk.Button, style_name: str):
        """Configure button hover effects."""
        original_bg = cls.STYLES[style_name]['bg']
        
        if style_name == 'button_primary':
            hover_bg = cls.COLORS['primary_hover']
        elif style_name == 'button_secondary':
            hover_bg = cls.COLORS['secondary_hover']
        else:
            hover_bg = original_bg
        
        def on_enter(event):
            button.configure(bg=hover_bg)
        
        def on_leave(event):
            button.configure(bg=original_bg)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)


class DarkTheme(ModernTheme):
    """
    Dark theme variant for users who prefer dark interfaces.
    """
    
    # Override colors for dark theme
    COLORS = {
        **ModernTheme.COLORS,
        'background': '#0f172a',
        'surface': '#1e293b',
        'surface_hover': '#334155',
        'border': '#475569',
        'text_primary': '#f8fafc',
        'text_secondary': '#cbd5e1',
        'text_muted': '#64748b',
    }
    
    # Update styles with dark colors
    STYLES = {
        **ModernTheme.STYLES,
        'window': {'bg': COLORS['background']},
        'main_frame': {'bg': COLORS['background'], 'relief': tk.FLAT},
        'timeline_frame': {
            'bg': COLORS['surface'],
            'relief': tk.FLAT,
            'bd': 1,
            'highlightbackground': COLORS['border'],
        },
        'timeline_text': {
            **ModernTheme.STYLES['timeline_text'],
            'bg': COLORS['background'],
            'fg': COLORS['text_primary'],
        },
        'input_text': {
            **ModernTheme.STYLES['input_text'],
            'bg': COLORS['surface'],
            'fg': COLORS['text_primary'],
            'highlightbackground': COLORS['border'],
        },
        'label_heading': {
            'bg': COLORS['background'],
            'fg': COLORS['text_primary'],
            'font': ModernTheme.FONTS['heading'],
        },
        'label_body': {
            'bg': COLORS['background'],
            'fg': COLORS['text_secondary'],
            'font': ModernTheme.FONTS['body'],
        },
    }