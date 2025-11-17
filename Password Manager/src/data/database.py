import sqlite3
import json
from typing import List, Optional
from pathlib import Path
from ..crypto.encryption import EncryptionManager
from .models import PasswordEntry

class DatabaseManager:
    def __init__(self, db_path: str, encryption_manager: EncryptionManager):
        self.db_path = Path(db_path)
        self.encryption_manager = encryption_manager
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS password_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT,
                    password TEXT NOT NULL,
                    url TEXT,
                    category TEXT DEFAULT 'General',
                    notes TEXT,
                    strength TEXT DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS app_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
    
    def add_entry(self, entry: PasswordEntry) -> int:
        """Add a new password entry"""
        encrypted_password = self.encryption_manager.encrypt(entry.password)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO password_entries 
                (title, username, email, password, url, category, notes, strength)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry.title, entry.username, entry.email, encrypted_password,
                entry.url, entry.category, entry.notes, entry.strength.value
            ))
            return cursor.lastrowid
    
    def get_all_entries(self) -> List[PasswordEntry]:
        """Retrieve all password entries"""
        entries = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM password_entries ORDER BY title')
            
            for row in cursor.fetchall():
                decrypted_password = self.encryption_manager.decrypt(row['password'])
                entries.append(PasswordEntry(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    email=row['email'],
                    password=decrypted_password,
                    url=row['url'],
                    category=row['category'],
                    notes=row['notes'],
                    strength=row['strength'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
        return entries
    
        def get_entry_by_id(self, entry_id: int) -> Optional[PasswordEntry]:
        """Get a specific password entry by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM password_entries WHERE id = ?', (entry_id,))
            row = cursor.fetchone()
            
            if row:
                decrypted_password = self.encryption_manager.decrypt(row['password'])
                return PasswordEntry(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    email=row['email'],
                    password=decrypted_password,
                    url=row['url'],
                    category=row['category'],
                    notes=row['notes'],
                    strength=row['strength'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None

    def update_entry(self, entry: PasswordEntry) -> bool:
        """Update an existing password entry"""
        if entry.id is None:
            return False
            
        encrypted_password = self.encryption_manager.encrypt(entry.password)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE password_entries 
                SET title=?, username=?, email=?, password=?, url=?, 
                    category=?, notes=?, strength=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (
                entry.title, entry.username, entry.email, encrypted_password,
                entry.url, entry.category, entry.notes, entry.strength.value, entry.id
            ))
            return cursor.rowcount > 0

    def delete_entry(self, entry_id: int) -> bool:
        """Delete a password entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM password_entries WHERE id = ?', (entry_id,))
            return cursor.rowcount > 0

    def search_entries(self, query: str) -> List[PasswordEntry]:
        """Search entries by title, username, or category"""
        search_term = f"%{query}%"
        entries = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM password_entries 
                WHERE title LIKE ? OR username LIKE ? OR category LIKE ?
                ORDER BY title
            ''', (search_term, search_term, search_term))
            
            for row in cursor.fetchall():
                decrypted_password = self.encryption_manager.decrypt(row['password'])
                entries.append(PasswordEntry(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    email=row['email'],
                    password=decrypted_password,
                    url=row['url'],
                    category=row['category'],
                    notes=row['notes'],
                    strength=row['strength'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
        return entries

    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT category FROM password_entries ORDER BY category')
            return [row[0] for row in cursor.fetchall()]

    def get_entries_by_category(self, category: str) -> List[PasswordEntry]:
        """Get all entries in a specific category"""
        entries = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM password_entries WHERE category = ? ORDER BY title', (category,))
            
            for row in cursor.fetchall():
                decrypted_password = self.encryption_manager.decrypt(row['password'])
                entries.append(PasswordEntry(
                    id=row['id'],
                    title=row['title'],
                    username=row['username'],
                    email=row['email'],
                    password=decrypted_password,
                    url=row['url'],
                    category=row['category'],
                    notes=row['notes'],
                    strength=row['strength'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
        return entries

    def export_to_csv(self, file_path: str) -> bool:
        """Export all entries to CSV (passwords remain encrypted)"""
        try:
            import csv
            entries = self.get_all_entries()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Title', 'Username', 'Email', 'URL', 'Category', 'Strength', 'Created'])
                
                for entry in entries:
                    writer.writerow([
                        entry.title,
                        entry.username,
                        entry.email or '',
                        entry.url or '',
                        entry.category,
                        entry.strength.value,
                        entry.created_at
                    ])
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False