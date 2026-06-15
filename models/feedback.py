"""
AI Feedback model definition.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Feedback:
    """
    Represents AI-generated feedback for an assignment.
    """
    id: str
    schedule_id: str
    user_id: str
    assignment_text: str
    overall_score: int  # 0-100
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "schedule_id": self.schedule_id,
            "user_id": self.user_id,
            "assignment_text": self.assignment_text,
            "overall_score": self.overall_score,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "suggestions": self.suggestions,
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def __repr__(self) -> str:
        return f"Feedback(score={self.overall_score}, schedule={self.schedule_id})"
