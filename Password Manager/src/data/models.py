from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class PasswordStrength(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"

class PasswordEntry(BaseModel):
    id: Optional[int] = None
    title: str
    username: str
    email: Optional[EmailStr] = None
    password: str  # Encrypted
    url: Optional[str] = None
    category: str = "General"
    notes: Optional[str] = None
    strength: PasswordStrength = PasswordStrength.MEDIUM
    created_at: datetime = None
    updated_at: datetime = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()