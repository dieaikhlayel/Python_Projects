import tkinter as tk
from tkinter import ttk, messagebox
from ...data.models import PasswordEntry, PasswordStrength
from ...crypto.password_generator import PasswordGenerator

class AddEntryDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        
        self.title("Add Password Entry")
        self.geometry("400x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.password_generator = PasswordGenerator()
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
        """Create form widgets"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Title:").pack(anchor=tk.W, pady=(0, 5))
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=40)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Username
        ttk.Label(main_frame, text="Username:").pack(anchor=tk.W, pady=(0, 5))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=40)
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=40)
        email_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(password_frame, text="Password:").pack(anchor=tk.W)
        
        password_input_frame = ttk.Frame(password_frame)
        password_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_input_frame, textvariable=self.password_var, 
                                       show="•", width=25)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_input_frame, text="Generate", 
                  command=self._generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(password_input_frame, text="Show", 
                  command=self._toggle_password_visibility).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Strength indicator
        self.strength_var = tk.StringVar(value="Strength: -")
        self.strength_label = ttk.Label(password_frame, textvariable=self.strength_var)
        self.strength_label.pack(anchor=tk.W, pady=(5, 0))
        
        # URL
        ttk.Label(main_frame, text="URL:").pack(anchor=tk.W, pady=(0, 5))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=40)
        url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Category
        ttk.Label(main_frame, text="Category:").pack(anchor=tk.W, pady=(0, 5))
        self.category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, 
                                     values=["General", "Social Media", "Email", "Banking", "Work", "Personal"])
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Notes
        ttk.Label(main_frame, text="Notes:").pack(anchor=tk.W, pady=(0, 5))
        self.notes_text = tk.Text(main_frame, height=4, width=40)
        self.notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save", command=self._save).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.RIGHT)
        
        # Bind password changes to strength calculation
        self.password_var.trace('w', self._update_strength)
        title_entry.focus()
    
    def _generate_password(self):
        """Generate a strong password"""
        password = self.password_generator.generate_from_preset(PasswordStrength.STRONG)
        self.password_var.set(password)
        self._update_strength()
    
    def _toggle_password_visibility(self):
        """Toggle password visibility"""
        current_show = self.password_entry.cget('show')
        self.password_entry.config(show='' if current_show else '•')
    
    def _update_strength(self, *args):
        """Update password strength indicator"""
        password = self.password_var.get()
        if password:
            strength = self.password_generator.assess_strength(password)
            self.strength_var.set(f"Strength: {strength.upper()}")
            
            # Update color based on strength
            colors = {
                "weak": "red",
                "medium": "orange",
                "strong": "green",
                "very_strong": "darkgreen"
            }
            self.strength_label.config(foreground=colors.get(strength, "black"))
        else:
            self.strength_var.set("Strength: -")
            self.strength_label.config(foreground="black")
    
    def _save(self):
        """Save the new password entry"""
        title = self.title_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        
        if not username:
            messagebox.showerror("Error", "Username is required")
            return
        
        if not password:
            messagebox.showerror("Error", "Password is required")
            return
        
        # Create PasswordEntry object
        entry = PasswordEntry(
            title=title,
            username=username,
            email=self.email_var.get().strip() or None,
            password=password,
            url=self.url_var.get().strip() or None,
            category=self.category_var.get(),
            notes=self.notes_text.get("1.0", tk.END).strip() or None,
            strength=PasswordStrength(self.password_generator.assess_strength(password))
        )
        
        self.result = entry
        self.destroy()
    
    def _cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.destroy()