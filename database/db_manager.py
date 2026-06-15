"""
Database manager for SQLite operations.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional

from models.schedule import Schedule
from models.user import User
from utils.logger import setup_logger
from database.schemas import SCHEMA

logger = setup_logger(__name__)


class DatabaseManager:
    """
    Manages SQLite database operations.
    """
    
    def __init__(self, db_path: str = "data/database.db"):
        """
        Initialize DatabaseManager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.cursor = None
        self.init_db()
    
    def init_db(self) -> None:
        """
        Initialize database connection and create tables.
        """
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.cursor = self.connection.cursor()
            
            # Create tables
            for schema in SCHEMA:
                self.cursor.execute(schema)
            
            self.connection.commit()
            logger.info(f"Database initialized: {self.db_path}")
        
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def create_schedule(self, schedule: Schedule) -> None:
        """
        Create a new schedule in the database.
        
        Args:
            schedule: Schedule object
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO schedules 
                (id, user_id, title, description, due_date, priority, category, is_completed, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    schedule.id,
                    schedule.user_id,
                    schedule.title,
                    schedule.description,
                    schedule.due_date.isoformat(),
                    schedule.priority,
                    schedule.category,
                    schedule.is_completed,
                    schedule.created_at.isoformat(),
                    schedule.updated_at.isoformat(),
                ),
            )
            self.connection.commit()
            logger.info(f"Schedule created: {schedule.id}")
        
        except sqlite3.Error as e:
            logger.error(f"Error creating schedule: {str(e)}")
            raise
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """
        Get a schedule by ID.
        
        Args:
            schedule_id: Schedule ID
        
        Returns:
            Schedule object or None
        """
        try:
            self.cursor.execute(
                "SELECT * FROM schedules WHERE id = ?",
                (schedule_id,),
            )
            row = self.cursor.fetchone()
            
            if row:
                return self._row_to_schedule(row)
            return None
        
        except sqlite3.Error as e:
            logger.error(f"Error getting schedule: {str(e)}")
            return None
    
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
        try:
            date_str = target_date.isoformat()
            self.cursor.execute(
                """
                SELECT * FROM schedules 
                WHERE user_id = ? AND DATE(due_date) = DATE(?)
                ORDER BY priority ASC, due_date ASC
                """,
                (user_id, date_str),
            )
            rows = self.cursor.fetchall()
            return [self._row_to_schedule(row) for row in rows]
        
        except sqlite3.Error as e:
            logger.error(f"Error getting schedules by date: {str(e)}")
            return []
    
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
        try:
            self.cursor.execute(
                """
                SELECT * FROM schedules 
                WHERE user_id = ? AND priority = ?
                ORDER BY due_date ASC
                """,
                (user_id, priority),
            )
            rows = self.cursor.fetchall()
            return [self._row_to_schedule(row) for row in rows]
        
        except sqlite3.Error as e:
            logger.error(f"Error getting schedules by priority: {str(e)}")
            return []
    
    def update_schedule(self, schedule_id: str, **kwargs) -> Schedule:
        """
        Update a schedule.
        
        Args:
            schedule_id: Schedule ID
            **kwargs: Fields to update
        
        Returns:
            Updated schedule
        """
        try:
            # Add updated_at timestamp
            kwargs["updated_at"] = datetime.now().isoformat()
            
            # Build update query
            set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            values = list(kwargs.values()) + [schedule_id]
            
            query = f"UPDATE schedules SET {set_clause} WHERE id = ?"
            self.cursor.execute(query, values)
            self.connection.commit()
            
            logger.info(f"Schedule updated: {schedule_id}")
            return self.get_schedule(schedule_id)
        
        except sqlite3.Error as e:
            logger.error(f"Error updating schedule: {str(e)}")
            raise
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: Schedule ID
        
        Returns:
            True if deleted successfully
        """
        try:
            self.cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
            self.connection.commit()
            logger.info(f"Schedule deleted: {schedule_id}")
            return True
        
        except sqlite3.Error as e:
            logger.error(f"Error deleting schedule: {str(e)}")
            return False
    
    def create_user(self, user: User) -> None:
        """
        Create a new user.
        
        Args:
            user: User object
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO users 
                (id, username, email, password_hash, name, grade, created_at, updated_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.id,
                    user.username,
                    user.email,
                    user.password_hash,
                    user.name,
                    user.grade,
                    user.created_at.isoformat(),
                    user.updated_at.isoformat(),
                    user.is_active,
                ),
            )
            self.connection.commit()
            logger.info(f"User created: {user.username}")
        
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User object or None
        """
        try:
            self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = self.cursor.fetchone()
            return self._row_to_user(row) if row else None
        
        except sqlite3.Error as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username.
        
        Args:
            username: Username
        
        Returns:
            User object or None
        """
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = self.cursor.fetchone()
            return self._row_to_user(row) if row else None
        
        except sqlite3.Error as e:
            logger.error(f"Error getting user by username: {str(e)}")
            return None
    
    def update_user(self, user_id: str, **kwargs) -> User:
        """
        Update a user.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
        
        Returns:
            Updated user
        """
        try:
            kwargs["updated_at"] = datetime.now().isoformat()
            set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            values = list(kwargs.values()) + [user_id]
            
            query = f"UPDATE users SET {set_clause} WHERE id = ?"
            self.cursor.execute(query, values)
            self.connection.commit()
            
            logger.info(f"User updated: {user_id}")
            return self.get_user(user_id)
        
        except sqlite3.Error as e:
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    @staticmethod
    def _row_to_schedule(row: tuple) -> Schedule:
        """
        Convert database row to Schedule object.
        
        Args:
            row: Database row tuple
        
        Returns:
            Schedule object
        """
        return Schedule(
            id=row[0],
            user_id=row[1],
            title=row[2],
            description=row[3],
            due_date=datetime.fromisoformat(row[4]),
            priority=row[5],
            category=row[6],
            is_completed=bool(row[7]),
            created_at=datetime.fromisoformat(row[8]),
            updated_at=datetime.fromisoformat(row[9]),
        )
    
    @staticmethod
    def _row_to_user(row: tuple) -> User:
        """
        Convert database row to User object.
        
        Args:
            row: Database row tuple
        
        Returns:
            User object
        """
        return User(
            id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            name=row[4],
            grade=row[5],
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7]),
            is_active=bool(row[8]),
        )
    
    def close(self) -> None:
        """
        Close database connection.
        """
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
