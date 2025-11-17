import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import os
from pathlib import Path
from ...crypto.key_derivation import verify_key, derive_key

class LoginDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.master_password = None
        
        self.title("Password Manager - Login")
        self.geometry("300x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self.center_on_parent(parent)
    
    def center_on_parent(self, parent):
        """Center the dialog on parent window"""
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create login form widgets"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Master Password", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Password entry
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="Password:").pack(anchor=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                       show="•", width=25)
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        self.password_entry.bind('<Return>', lambda e: self._login())
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Login", command=self._login).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.RIGHT)
        
        # Focus password entry
        self.password_entry.focus()
    
    def _login(self):
        """Attempt login with master password"""
        password = self.password_var.get().strip()
        
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return
        
        if len(password) < 8:
            messagebox.showerror("Error", "Master password must be at least 8 characters")
            return
        
        # For first-time setup, we'll create the vault
        # In a real app, you'd verify against a stored hash
        self.master_password = password
        self.result = True
        self.destroy()
    
    def _cancel(self):
        """Cancel login"""
        self.result = False
        self.destroy()