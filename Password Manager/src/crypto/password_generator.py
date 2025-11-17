import random
import string
import secrets
from typing import List
from enum import Enum

class PasswordPreset(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length: int = 16, use_lowercase: bool = True, 
                 use_uppercase: bool = True, use_digits: bool = True, 
                 use_special: bool = True) -> str:
        """Generate a cryptographically secure random password"""
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        char_pool = ""
        if use_lowercase:
            char_pool += self.lowercase
        if use_uppercase:
            char_pool += self.uppercase
        if use_digits:
            char_pool += self.digits
        if use_special:
            char_pool += self.special_chars
        
        if not char_pool:
            raise ValueError("At least one character type must be selected")
        
        # Ensure at least one character from each selected type
        password_chars = []
        if use_lowercase:
            password_chars.append(secrets.choice(self.lowercase))
        if use_uppercase:
            password_chars.append(secrets.choice(self.uppercase))
        if use_digits:
            password_chars.append(secrets.choice(self.digits))
        if use_special:
            password_chars.append(secrets.choice(self.special_chars))
        
        # Fill remaining length with random characters from the pool
        remaining_length = length - len(password_chars)
        password_chars.extend(secrets.choice(char_pool) for _ in range(remaining_length))
        
        # Shuffle the password characters
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_from_preset(self, preset: PasswordPreset) -> str:
        """Generate password using predefined presets"""
        presets = {
            PasswordPreset.WEAK: (12, True, True, False, False),
            PasswordPreset.MEDIUM: (14, True, True, True, False),
            PasswordPreset.STRONG: (16, True, True, True, True),
            PasswordPreset.VERY_STRONG: (20, True, True, True, True)
        }
        
        length, lower, upper, digits, special = presets[preset]
        return self.generate(length, lower, upper, digits, special)
    
    def assess_strength(self, password: str) -> str:
        """Assess password strength"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if any(c in string.ascii_lowercase for c in password):
            score += 1
        if any(c in string.ascii_uppercase for c in password):
            score += 1
        if any(c in string.digits for c in password):
            score += 1
        if any(c in self.special_chars for c in password):
            score += 1
        
        if score <= 2:
            return "weak"
        elif score <= 4:
            return "medium"
        elif score <= 5:
            return "strong"
        else:
            return "very_strong"