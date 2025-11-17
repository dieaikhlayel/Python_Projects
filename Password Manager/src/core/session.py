import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable

class SessionManager:
    def __init__(self, master_password: str, auto_lock_minutes: int = 15):
        self.master_password = master_password
        self.auto_lock_minutes = auto_lock_minutes
        self.login_time = datetime.now()
        self.last_activity = datetime.now()
        self.is_locked = False
        self._activity_callbacks = []
        self._lock_callbacks = []
        
        # Start auto-lock timer
        self._start_auto_lock_timer()
    
    def _start_auto_lock_timer(self):
        """Start background thread for auto-locking"""
        def auto_lock_check():
            while True:
                time.sleep(30)  # Check every 30 seconds
                if not self.is_locked:
                    idle_time = datetime.now() - self.last_activity
                    if idle_time > timedelta(minutes=self.auto_lock_minutes):
                        self.lock()
        
        timer_thread = threading.Thread(target=auto_lock_check, daemon=True)
        timer_thread.start()
    
    def record_activity(self):
        """Record user activity to prevent auto-lock"""
        self.last_activity = datetime.now()
        for callback in self._activity_callbacks:
            callback()
    
    def lock(self):
        """Lock the session"""
        self.is_locked = True
        for callback in self._lock_callbacks:
            callback()
    
    def unlock(self, password: str) -> bool:
        """Unlock the session with master password"""
        if password == self.master_password:
            self.is_locked = False
            self.last_activity = datetime.now()
            return True
        return False
    
    def get_session_duration(self) -> timedelta:
        """Get how long the session has been active"""
        return datetime.now() - self.login_time
    
    def get_idle_time(self) -> timedelta:
        """Get how long the session has been idle"""
        return datetime.now() - self.last_activity
    
    def add_activity_callback(self, callback: Callable):
        """Add callback for activity events"""
        self._activity_callbacks.append(callback)
    
    def add_lock_callback(self, callback: Callable):
        """Add callback for lock events"""
        self._lock_callbacks.append(callback)
    
    def change_master_password(self, old_password: str, new_password: str) -> bool:
        """Change the master password"""
        if old_password == self.master_password and len(new_password) >= 8:
            self.master_password = new_password
            return True
        return False