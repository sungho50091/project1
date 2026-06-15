"""
Schedule model definition.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Schedule:
    """
    Represents a study schedule or assignment.
    """
    id: str
    user_id: str
    title: str
    description: str
    due_date: datetime
    priority: str  # 'high', 'medium', 'low'
    category: str  # 'homework', 'exam', 'project', etc.
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    ai_feedback_id: Optional[str] = None
    tags: list = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "category": self.category,
            "is_completed": self.is_completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "ai_feedback_id": self.ai_feedback_id,
            "tags": self.tags,
        }
    
    def __repr__(self) -> str:
        return f"Schedule({self.title}, due={self.due_date}, priority={self.priority})"
