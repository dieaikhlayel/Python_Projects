import tkinter as tk
import threading
import time
from typing import Optional

class ClipboardManager:
    def __init__(self, clear_after_seconds: int = 30):
        self.clear_after_seconds = clear_after_seconds
        self._clear_timer: Optional[threading.Timer] = None
        self._last_copied_text: Optional[str] = None
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard and schedule clearing"""
        try:
            # Clear existing timer
            if self._clear_timer:
                self._clear_timer.cancel()
            
            # Copy to clipboard
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()
            root.destroy()
            
            self._last_copied_text = text
            
            # Schedule clearing if enabled
            if self.clear_after_seconds > 0:
                self._clear_timer = threading.Timer(self.clear_after_seconds, self.clear_clipboard)
                self._clear_timer.daemon = True
                self._clear_timer.start()
            
            print(f"Copied to clipboard (will clear in {self.clear_after_seconds}s)")
            
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
    
    def clear_clipboard(self):
        """Clear the clipboard"""
        try:
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.update()
            root.destroy()
            
            self._last_copied_text = None
            print("Clipboard cleared")
            
        except Exception as e:
            print(f"Failed to clear clipboard: {e}")
    
    def get_last_copied(self) -> Optional[str]:
        """Get the last copied text"""
        return self._last_copied_text
    
    def set_clear_timeout(self, seconds: int):
        """Set the clipboard clear timeout"""
        self.clear_after_seconds = seconds
        
        # Restart timer if there's text in clipboard
        if self._last_copied_text and self._clear_timer:
            self._clear_timer.cancel()
            if seconds > 0:
                self._clear_timer = threading.Timer(seconds, self.clear_clipboard)
                self._clear_timer.daemon = True
                self._clear_timer.start()