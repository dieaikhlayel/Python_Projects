import unittest
import os
from src.crypto.key_derivation import generate_salt, derive_key
from src.crypto.encryption import EncryptionManager

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.master_password = "test_password_123"
        self.salt = generate_salt()
        self.encryption_manager = EncryptionManager(self.master_password, self.salt)
    
    def test_encryption_decryption(self):
        """Test that encryption and decryption work correctly"""
        original_text = "This is a secret message"
        
        # Encrypt
        encrypted = self.encryption_manager.encrypt(original_text)
        
        # Verify it's different from original
        self.assertNotEqual(encrypted, original_text)
        
        # Decrypt
        decrypted = self.encryption_manager.decrypt(encrypted)
        
        # Verify it matches original
        self.assertEqual(decrypted, original_text)
    
    def test_different_salts_produce_different_keys(self):
        """Test that different salts produce different encryption results"""
        salt2 = generate_salt()
        encryption_manager2 = EncryptionManager(self.master_password, salt2)
        
        original_text = "Test message"
        
        encrypted1 = self.encryption_manager.encrypt(original_text)
        encrypted2 = encryption_manager2.encrypt(original_text)
        
        # Should be different due to different salts
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails decryption"""
        original_text = "Secret data"
        encrypted = self.encryption_manager.encrypt(original_text)
        
        # Create manager with wrong password
        wrong_manager = EncryptionManager("wrong_password", self.salt)
        
        # Should raise an exception or return garbage
        with self.assertRaises(Exception):
            wrong_manager.decrypt(encrypted)

if __name__ == '__main__':
    unittest.main()