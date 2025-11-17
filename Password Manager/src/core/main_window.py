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