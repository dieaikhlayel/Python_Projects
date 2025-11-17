import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.simpledialog as simpledialog
from typing import List
from ..data.models import PasswordEntry
from ..crypto.password_generator import PasswordGenerator

class MainWindow(tk.Tk):
    def __init__(self, db_manager, session):
        super().__init__()
        self.db_manager = db_manager
        self.session = session
        self.password_entries: List[PasswordEntry] = []
        
        self.title("Secure Password Manager")
        self.geometry("800x600")
        self.configure(bg='#2b2b2b')
        
        self._setup_styles()
        self._create_widgets()
        self._load_entries()
    
    def _setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for dark theme
        style.configure('Treeview', 
                       background='#3c3f41',
                       foreground='white',
                       fieldbackground='#3c3f41')
        
        style.configure('TButton', padding=6, relief='flat', background='#4caf50')
        style.configure('TFrame', background='#2b2b2b')
    
    def _create_widgets(self):
        """Create main window widgets"""
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Entry", command=self._add_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Generate Password", command=self._generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self._load_entries).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self._on_search)
        
        # Treeview for password entries
        columns = ('Title', 'Username', 'Category', 'Strength')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self._on_item_double_click)
    
    def _load_entries(self):
        """Load password entries into treeview"""
        self.tree.delete(*self.tree.get_children())
        self.password_entries = self.db_manager.get_all_entries()
        
        for entry in self.password_entries:
            self.tree.insert('', tk.END, values=(
                entry.title, entry.username, entry.category, entry.strength.value
            ))
    
    def _add_entry(self):
        """Open add entry dialog"""
        from .add_entry_dialog import AddEntryDialog
        dialog = AddEntryDialog(self)
        if dialog.result:
            self.db_manager.add_entry(dialog.result)
            self._load_entries()
    
    def _generate_password(self):
        """Generate a strong password"""
        generator = PasswordGenerator()
        password = generator.generate(16)
        messagebox.showinfo("Generated Password", f"Your new password:\n{password}")
    
    def _on_search(self, event):
        """Filter entries based on search"""
        search_term = self.search_var.get().lower()
        
        self.tree.delete(*self.tree.get_children())
        for entry in self.password_entries:
            if (search_term in entry.title.lower() or 
                search_term in entry.username.lower() or
                search_term in entry.category.lower()):
                
                self.tree.insert('', tk.END, values=(
                    entry.title, entry.username, entry.category, entry.strength.value
                ))
    
    def _on_item_double_click(self, event):
        """Show entry details on double click"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Find the complete entry
            title = values[0]
            entry = next((e for e in self.password_entries if e.title == title), None)
            
            if entry:
                self._show_entry_details(entry)
     
        def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export to CSV...", command=self._export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Backup Database...", command=self._backup_database)
        file_menu.add_command(label="Restore from Backup...", command=self._restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Password Generator", command=self._generate_password)
        tools_menu.add_command(label="Strength Checker", command=self._check_strength)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
    
    def _show_entry_details(self, entry: PasswordEntry):
        """Show detailed view of a password entry"""
        from tkinter import Toplevel, Label, Frame, Button
        from ..utils.clipboard import ClipboardManager
        
        details_window = Toplevel(self)
        details_window.title(f"Details - {entry.title}")
        details_window.geometry("400x300")
        details_window.transient(self)
        details_window.grab_set()
        
        # Create clipboard manager
        clipboard = ClipboardManager(self.config.get('security.clear_clipboard_seconds'))
        
        # Details frame
        main_frame = Frame(details_window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Display entry details
        details = [
            ("Title:", entry.title),
            ("Username:", entry.username),
            ("Email:", entry.email or "Not set"),
            ("URL:", entry.url or "Not set"),
            ("Category:", entry.category),
            ("Strength:", entry.strength.value.upper()),
            ("Created:", entry.created_at.strftime("%Y-%m-%d %H:%M")),
            ("Updated:", entry.updated_at.strftime("%Y-%m-%d %H:%M")),
        ]
        
        for i, (label, value) in enumerate(details):
            Label(main_frame, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='w', pady=2)
            Label(main_frame, text=value).grid(row=i, column=1, sticky='w', pady=2, padx=(10, 0))
        
        # Notes
        if entry.notes:
            Label(main_frame, text="Notes:", font=('Arial', 10, 'bold')).grid(row=len(details), column=0, sticky='nw', pady=(10, 2))
            notes_text = Text(main_frame, height=4, width=40, wrap='word')
            notes_text.grid(row=len(details), column=1, sticky='we', pady=(10, 2), padx=(10, 0))
            notes_text.insert('1.0', entry.notes)
            notes_text.config(state='disabled')
        
        # Button frame
        button_frame = Frame(main_frame)
        button_frame.grid(row=len(details) + 2, column=0, columnspan=2, pady=(20, 0), sticky='we')
        
        Button(button_frame, text="Copy Username", 
              command=lambda: clipboard.copy_to_clipboard(entry.username)).pack(side='left', padx=(0, 5))
        Button(button_frame, text="Copy Password", 
              command=lambda: clipboard.copy_to_clipboard(entry.password)).pack(side='left', padx=5)
        Button(button_frame, text="Edit", 
              command=lambda: self._edit_entry(entry, details_window)).pack(side='left', padx=5)
        Button(button_frame, text="Close", 
              command=details_window.destroy).pack(side='right')
    
    def _edit_entry(self, entry: PasswordEntry, parent_window):
        """Edit an existing entry"""
        from .add_entry_dialog import AddEntryDialog
        
        # Close details window
        parent_window.destroy()
        
        # Open edit dialog (you'd need to modify AddEntryDialog to support editing)
        # This is a simplified version
        dialog = AddEntryDialog(self)
        if dialog.result:
            dialog.result.id = entry.id  # Preserve the ID
            self.db_manager.update_entry(dialog.result)
            self._load_entries()
    
    def _export_csv(self):
        """Export entries to CSV"""
        from tkinter import filedialog
        import os
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            success = self.db_manager.export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", f"Entries exported to {os.path.basename(filename)}")
            else:
                messagebox.showerror("Error", "Failed to export entries")
    
    def _show_settings(self):
        """Show settings dialog"""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self, self.config)
        if dialog.result:
            # Settings were saved, reload if needed
            pass
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """Secure Password Manager

Version 1.0.0

A secure, local password manager with encryption
and cloud backup capabilities.

Built with Python and tkinter.

© 2024 Your Name"""
        
        messagebox.showinfo("About", about_text)