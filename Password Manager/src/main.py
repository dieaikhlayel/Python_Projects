import tkinter as tk
from gui.main_window import MainWindow
from gui.login_dialog import LoginDialog
from data.database import DatabaseManager
from crypto.encryption import EncryptionManager
from crypto.key_derivation import derive_key, generate_salt
from core.config import ConfigManager
from core.session import SessionManager
import os

class PasswordManagerApp:
    def __init__(self):
        self.config = ConfigManager()
        self.session = None
        self.db_manager = None
        self.encryption_manager = None
        
    def run(self):
        """Start the application"""
        # Show login dialog
        root = tk.Tk()
        root.withdraw()  # Hide main window initially
        
        login_dialog = LoginDialog(root)
        if login_dialog.result:
            self._initialize_managers(login_dialog.master_password)
            self._show_main_window()
        else:
            print("Login cancelled")
            
    def _initialize_managers(self, master_password: str):
        """Initialize all managers with the master password"""
        # Get or create encryption salt
        salt = self._get_encryption_salt()
        
        # Initialize encryption
        self.encryption_manager = EncryptionManager(master_password, salt)
        
        # Initialize database
        db_path = self.config.get('database.path')
        self.db_manager = DatabaseManager(db_path, self.encryption_manager)
        
        # Initialize session
        self.session = SessionManager(master_password)
        
    def _get_encryption_salt(self) -> bytes:
        """Get existing salt or generate new one"""
        salt_file = Path('data/salt.bin')
        salt_file.parent.mkdir(exist_ok=True)
        
        if salt_file.exists():
            return salt_file.read_bytes()
        else:
            salt = generate_salt()
            salt_file.write_bytes(salt)
            return salt
            
    def _show_main_window(self):
        """Show the main application window"""
        root = tk.Tk()
        app = MainWindow(self.db_manager, self.session)
        app.mainloop()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.run()