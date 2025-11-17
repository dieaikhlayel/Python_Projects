import re
from typing import Optional, Tuple
from urllib.parse import urlparse

class InputValidators:
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        # Check for common patterns
        common_patterns = [
            r'12345678',
            r'password',
            r'qwertyui',
            r'00000000',
            r'11111111'
        ]
        
        for pattern in common_patterns:
            if pattern in password.lower():
                return False, "Password contains common weak patterns"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """Validate email format"""
        if not email:  # Email is optional
            return True, None
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, None
        else:
            return False, "Invalid email format"
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """Validate URL format"""
        if not url:  # URL is optional
            return True, None
            
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                return True, None
            else:
                return False, "Invalid URL format"
        except Exception:
            return False, "Invalid URL format"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """Validate username"""
        if not username.strip():
            return False, "Username cannot be empty"
        
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        
        # Check for potentially dangerous characters
        if re.search(r'[<>"\'&]', username):
            return False, "Username contains invalid characters"
        
        return True, None
    
    @staticmethod
    def validate_title(title: str) -> Tuple[bool, Optional[str]]:
        """Validate entry title"""
        if not title.strip():
            return False, "Title cannot be empty"
        
        if len(title) > 100:
            return False, "Title must be less than 100 characters"
        
        return True, None