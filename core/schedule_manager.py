"""
Schedule management business logic.

Handles CRUD operations for schedules.
"""

from datetime import datetime, date
from typing import List, Optional
from uuid import uuid4

from models.schedule import Schedule
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScheduleManager:
    """
    Manages schedule-related operations.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize ScheduleManager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_schedule(
        self,
        user_id: str,
        title: str,
        description: str,
        due_date: datetime,
        priority: str,
        category: str,
    ) -> Schedule:
        """
        Create a new schedule.
        
        Args:
            user_id: User ID
            title: Schedule title
            description: Schedule description
            due_date: Due date
            priority: Priority level ('high', 'medium', 'low')
            category: Category (e.g., 'homework', 'exam', 'project')
        
        Returns:
            Schedule: Created schedule object
        
        Raises:
            ValueError: If input validation fails
        """
        if not title or len(title) < 1:
            raise ValueError("Title cannot be empty")
        
        if priority not in ["high", "medium", "low"]:
            raise ValueError(f"Invalid priority: {priority}")
        
        schedule = Schedule(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category,
            is_completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        logger.info(f"Creating schedule: {title}")
        self.db.create_schedule(schedule)
        return schedule
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """
        Get a schedule by ID.
        
        Args:
            schedule_id: Schedule ID
        
        Returns:
            Schedule or None if not found
        """
        return self.db.get_schedule(schedule_id)
    
    def get_schedules_by_date(
        self,
        user_id: str,
        target_date: date,
    ) -> List[Schedule]:
        """
        Get schedules for a specific date.
        
        Args:
            user_id: User ID
            target_date: Target date
        
        Returns:
            List of schedules
        """
        return self.db.get_schedules_by_date(user_id, target_date)
    
    def get_schedules_by_priority(
        self,
        user_id: str,
        priority: str,
    ) -> List[Schedule]:
        """
        Get schedules by priority level.
        
        Args:
            user_id: User ID
            priority: Priority level
        
        Returns:
            List of schedules
        """
        return self.db.get_schedules_by_priority(user_id, priority)
    
    def update_schedule(
        self,
        schedule_id: str,
        **kwargs,
    ) -> Schedule:
        """
        Update a schedule.
        
        Args:
            schedule_id: Schedule ID
            **kwargs: Fields to update
        
        Returns:
            Updated schedule
        """
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule {schedule_id} not found")
        
        logger.info(f"Updating schedule: {schedule_id}")
        return self.db.update_schedule(schedule_id, **kwargs)
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: Schedule ID
        
        Returns:
            True if deleted successfully
        """
        logger.info(f"Deleting schedule: {schedule_id}")
        return self.db.delete_schedule(schedule_id)
    
    def mark_completed(
        self,
        schedule_id: str,
        is_completed: bool = True,
    ) -> Schedule:
        """
        Mark a schedule as completed.
        
        Args:
            schedule_id: Schedule ID
            is_completed: Completion status
        
        Returns:
            Updated schedule
        """
        return self.update_schedule(
            schedule_id,
            is_completed=is_completed,
            updated_at=datetime.now(),
        )
