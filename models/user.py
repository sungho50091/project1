"""
User model definition.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Represents a user account.
    """
    id: str
    username: str
    email: str
    password_hash: str
    name: str
    grade: Optional[int] = None  # School grade
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    preferences: dict = field(default_factory=dict)
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive data
        
        Returns:
            Dictionary representation
        """
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "grade": self.grade,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "preferences": self.preferences,
        }
        
        if include_sensitive:
            data["password_hash"] = self.password_hash
        
        return data
    
    def __repr__(self) -> str:
        return f"User({self.username}, {self.name}, grade={self.grade})"
