"""
Reminder and notification service.

Handles scheduling and delivery of reminders.
"""

from datetime import datetime, timedelta
from typing import Optional, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ReminderService:
    """
    Manages reminders and notifications.
    """
    
    def __init__(self):
        """
        Initialize ReminderService.
        """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self._reminders = {}  # Store active reminders
    
    def schedule_reminder(
        self,
        reminder_id: str,
        due_date: datetime,
        callback: Callable,
        lead_time_minutes: int = 30,
    ) -> None:
        """
        Schedule a reminder.
        
        Args:
            reminder_id: Unique reminder identifier
            due_date: When the task is due
            callback: Function to call when reminder triggers
            lead_time_minutes: Minutes before due date to trigger reminder
        """
        reminder_time = due_date - timedelta(minutes=lead_time_minutes)
        
        if reminder_time <= datetime.now():
            logger.warning(f"Reminder time {reminder_time} is in the past")
            return
        
        try:
            job = self.scheduler.add_job(
                func=callback,
                trigger="date",
                run_date=reminder_time,
                id=reminder_id,
            )
            self._reminders[reminder_id] = job
            logger.info(f"Reminder scheduled: {reminder_id} at {reminder_time}")
        
        except Exception as e:
            logger.error(f"Error scheduling reminder: {str(e)}")
    
    def cancel_reminder(self, reminder_id: str) -> bool:
        """
        Cancel a scheduled reminder.
        
        Args:
            reminder_id: Reminder ID
        
        Returns:
            True if cancelled successfully
        """
        try:
            if reminder_id in self._reminders:
                self.scheduler.remove_job(reminder_id)
                del self._reminders[reminder_id]
                logger.info(f"Reminder cancelled: {reminder_id}")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error cancelling reminder: {str(e)}")
            return False
    
    def reschedule_reminder(
        self,
        reminder_id: str,
        new_due_date: datetime,
        callback: Callable,
        lead_time_minutes: int = 30,
    ) -> None:
        """
        Reschedule an existing reminder.
        
        Args:
            reminder_id: Reminder ID
            new_due_date: New due date
            callback: Callback function
            lead_time_minutes: Minutes before due date
        """
        self.cancel_reminder(reminder_id)
        self.schedule_reminder(
            reminder_id,
            new_due_date,
            callback,
            lead_time_minutes,
        )
    
    def shutdown(self) -> None:
        """
        Shutdown the reminder service.
        """
        self.scheduler.shutdown()
        logger.info("Reminder service shut down")
