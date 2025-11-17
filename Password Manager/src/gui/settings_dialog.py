import tkinter as tk
from tkinter import ttk, messagebox
from ...core.config import ConfigManager

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config
        self.result = False
        
        self.title("Settings")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_current_settings()
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
        """Create settings widgets"""
        # Notebook for categories
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General Tab
        general_frame = ttk.Frame(notebook, padding=10)
        notebook.add(general_frame, text="General")
        
        # Theme
        ttk.Label(general_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, 
                                  values=["dark", "light"], state="readonly", width=20)
        theme_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Auto-lock
        ttk.Label(general_frame, text="Auto-lock (minutes):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.auto_lock_var = tk.StringVar()
        auto_lock_spin = ttk.Spinbox(general_frame, textvariable=self.auto_lock_var, 
                                    from_=1, to=120, width=10)
        auto_lock_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Security Tab
        security_frame = ttk.Frame(notebook, padding=10)
        notebook.add(security_frame, text="Security")
        
        # Clear clipboard
        ttk.Label(security_frame, text="Clear clipboard after (seconds):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.clipboard_clear_var = tk.StringVar()
        clipboard_spin = ttk.Spinbox(security_frame, textvariable=self.clipboard_clear_var, 
                                    from_=0, to=300, width=10)
        clipboard_spin.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(security_frame, text="(0 = never clear)").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Minimum password length
        ttk.Label(security_frame, text="Minimum password length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.min_password_var = tk.StringVar()
        min_password_spin = ttk.Spinbox(security_frame, textvariable=self.min_password_var, 
                                       from_=8, to=32, width=10)
        min_password_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Cloud Tab
        cloud_frame = ttk.Frame(notebook, padding=10)
        notebook.add(cloud_frame, text="Cloud")
        
        self.cloud_sync_var = tk.BooleanVar()
        cloud_check = ttk.Checkbutton(cloud_frame, text="Enable cloud synchronization", 
                                     variable=self.cloud_sync_var)
        cloud_check.grid(row=0, column=0, sticky=tk.W, pady=5, columnspan=2)
        
        ttk.Label(cloud_frame, text="Sync interval (minutes):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sync_interval_var = tk.StringVar()
        sync_interval_spin = ttk.Spinbox(cloud_frame, textvariable=self.sync_interval_var, 
                                        from_=5, to=1440, width=10)
        sync_interval_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self._save).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self._cancel).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Reset to Defaults", command=self._reset_defaults).pack(side=tk.LEFT)
    
    def _load_current_settings(self):
        """Load current settings into the form"""
        self.theme_var.set(self.config.get('gui.theme'))
        self.auto_lock_var.set(str(self.config.get('security.auto_lock_minutes')))
        self.clipboard_clear_var.set(str(self.config.get('security.clear_clipboard_seconds')))
        self.min_password_var.set(str(self.config.get('security.min_password_length')))
        self.cloud_sync_var.set(self.config.get('cloud.enable_sync'))
        self.sync_interval_var.set(str(self.config.get('cloud.sync_interval', 60) // 60))
    
    def _save(self):
        """Save settings"""
        try:
            # Validate inputs
            auto_lock = int(self.auto_lock_var.get())
            clipboard_clear = int(self.clipboard_clear_var.get())
            min_password = int(self.min_password_var.get())
            sync_interval = int(self.sync_interval_var.get()) * 60  # Convert to seconds
            
            if auto_lock < 1 or auto_lock > 120:
                messagebox.showerror("Error", "Auto-lock must be between 1 and 120 minutes")
                return
            
            if clipboard_clear < 0 or clipboard_clear > 300:
                messagebox.showerror("Error", "Clipboard clear must be between 0 and 300 seconds")
                return
            
            if min_password < 8 or min_password > 32:
                messagebox.showerror("Error", "Minimum password length must be between 8 and 32")
                return
            
            if sync_interval < 300 or sync_interval > 86400:
                messagebox.showerror("Error", "Sync interval must be between 5 minutes and 24 hours")
                return
            
            # Save settings
            self.config.set('gui.theme', self.theme_var.get())
            self.config.set('security.auto_lock_minutes', auto_lock)
            self.config.set('security.clear_clipboard_seconds', clipboard_clear)
            self.config.set('security.min_password_length', min_password)
            self.config.set('cloud.enable_sync', self.cloud_sync_var.get())
            self.config.set('cloud.sync_interval', sync_interval)
            
            self.result = True
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers in all fields")
    
    def _reset_defaults(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm", "Reset all settings to default values?"):
            self.theme_var.set("dark")
            self.auto_lock_var.set("15")
            self.clipboard_clear_var.set("30")
            self.min_password_var.set("8")
            self.cloud_sync_var.set(False)
            self.sync_interval_var.set("60")
    
    def _cancel(self):
        """Cancel without saving"""
        self.result = False
        self.destroy()