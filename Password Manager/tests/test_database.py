import unittest
import tempfile
import os
from src.data.database import DatabaseManager
from src.data.models import PasswordEntry, PasswordStrength
from src.crypto.encryption import EncryptionManager
from src.crypto.key_derivation import generate_salt

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        
        # Create encryption manager
        self.salt = generate_salt()
        self.encryption_manager = EncryptionManager("test_password", self.salt)
        self.db_manager = DatabaseManager(self.db_path, self.encryption_manager)
    
    def tearDown(self):
        # Clean up temporary database
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_add_and_retrieve_entry(self):
        """Test adding and retrieving a password entry"""
        entry = PasswordEntry(
            title="Test Account",
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            url="https://example.com",
            category="Testing",
            notes="Test notes",
            strength=PasswordStrength.STRONG
        )
        
        # Add entry
        entry_id = self.db_manager.add_entry(entry)
        self.assertIsNotNone(entry_id)
        
        # Retrieve all entries
        entries = self.db_manager.get_all_entries()
        self.assertEqual(len(entries), 1)
        
        # Verify data
        retrieved = entries[0]
        self.assertEqual(retrieved.title, entry.title)
        self.assertEqual(retrieved.username, entry.username)
        self.assertEqual(retrieved.email, entry.email)
        self.assertEqual(retrieved.password, entry.password)  # Should be decrypted
        self.assertEqual(retrieved.url, entry.url)
        self.assertEqual(retrieved.category, entry.category)
        self.assertEqual(retrieved.notes, entry.notes)
        self.assertEqual(retrieved.strength, entry.strength)
    
    def test_search_entries(self):
        """Test searching entries"""
        # Add test entries
        entries = [
            PasswordEntry(title="Gmail", username="user1", password="pass1", category="Email"),
            PasswordEntry(title="Facebook", username="user2", password="pass2", category="Social"),
            PasswordEntry(title="GitHub", username="user3", password="pass3", category="Development"),
        ]
        
        for entry in entries:
            self.db_manager.add_entry(entry)
        
        # Search by title
        results = self.db_manager.search_entries("mail")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Gmail")
        
        # Search by category
        results = self.db_manager.search_entries("social")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Facebook")
    
    def test_update_entry(self):
        """Test updating an entry"""
        entry = PasswordEntry(
            title="Original Title",
            username="originaluser",
            password="originalpass",
            category="Original"
        )
        
        entry_id = self.db_manager.add_entry(entry)
        entry.id = entry_id
        
        # Update entry
        entry.title = "Updated Title"
        entry.username = "updateduser"
        entry.password = "updatedpass"
        
        success = self.db_manager.update_entry(entry)
        self.assertTrue(success)
        
        # Verify update
        entries = self.db_manager.get_all_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, "Updated Title")
        self.assertEqual(entries[0].username, "updateduser")
        self.assertEqual(entries[0].password, "updatedpass")
    
    def test_delete_entry(self):
        """Test deleting an entry"""
        entry = PasswordEntry(
            title="To Delete",
            username="deleteuser",
            password="deletepass",
            category="Test"
        )
        
        entry_id = self.db_manager.add_entry(entry)
        
        # Verify entry exists
        entries = self.db_manager.get_all_entries()
        self.assertEqual(len(entries), 1)
        
        # Delete entry
        success = self.db_manager.delete_entry(entry_id)
        self.assertTrue(success)
        
        # Verify deletion
        entries = self.db_manager.get_all_entries()
        self.assertEqual(len(entries), 0)

if __name__ == '__main__':
    unittest.main()