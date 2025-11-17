import tkinter as tk
from tkinter import ttk

class StyleManager:
    def __init__(self):
        self.style = ttk.Style()
        self._setup_themes()
    
    def _setup_themes(self):
        """Setup light and dark themes"""
        # Dark theme
        self.style.theme_create('dark', parent='clam', settings={
            'TFrame': {
                'configure': {'background': '#2b2b2b'}
            },
            'TLabel': {
                'configure': {
                    'background': '#2b2b2b',
                    'foreground': '#ffffff',
                    'font': ('Arial', 10)
                }
            },
            'TButton': {
                'configure': {
                    'background': '#3c3c3c',
                    'foreground': '#ffffff',
                    'font': ('Arial', 10),
                    'borderwidth': 1,
                    'focuscolor': 'none'
                },
                'map': {
                    'background': [('active', '#4c4c4c'), ('pressed', '#5c5c5c')],
                    'foreground': [('active', '#ffffff')]
                }
            },
            'TEntry': {
                'configure': {
                    'fieldbackground': '#3c3c3c',
                    'foreground': '#ffffff',
                    'insertcolor': '#ffffff',
                    'borderwidth': 1
                }
            },
            'TCombobox': {
                'configure': {
                    'fieldbackground': '#3c3c3c',
                    'foreground': '#ffffff',
                    'background': '#3c3c3c'
                },
                'map': {
                    'fieldbackground': [('readonly', '#3c3c3c')],
                    'selectbackground': [('readonly', '#4c4c4c')]
                }
            },
            'Treeview': {
                'configure': {
                    'background': '#3c3c3c',
                    'foreground': '#ffffff',
                    'fieldbackground': '#3c3c3c'
                },
                'map': {
                    'background': [('selected', '#4c4c4c')],
                    'foreground': [('selected', '#ffffff')]
                }
            }
        })
        
        # Light theme
        self.style.theme_create('light', parent='clam', settings={
            'TFrame': {
                'configure': {'background': '#f0f0f0'}
            },
            'TLabel': {
                'configure': {
                    'background': '#f0f0f0',
                    'foreground': '#000000',
                    'font': ('Arial', 10)
                }
            },
            'TButton': {
                'configure': {
                    'background': '#e0e0e0',
                    'foreground': '#000000',
                    'font': ('Arial', 10),
                    'borderwidth': 1,
                    'focuscolor': 'none'
                },
                'map': {
                    'background': [('active', '#d0d0d0'), ('pressed', '#c0c0c0')],
                    'foreground': [('active', '#000000')]
                }
            }
        })
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in ['light', 'dark']:
            self.style.theme_use(theme_name)