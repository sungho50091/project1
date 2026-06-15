"""
Tests for ScheduleManager.
"""

import pytest
from datetime import datetime, timedelta

from core.schedule_manager import ScheduleManager
from database.db_manager import DatabaseManager
from models.schedule import Schedule


@pytest.fixture
def db_manager():
    """Create in-memory database for testing."""
    return DatabaseManager(":memory:")


@pytest.fixture
def schedule_manager(db_manager):
    """Create schedule manager with test database."""
    return ScheduleManager(db_manager)


def test_create_schedule(schedule_manager):
    """Test creating a schedule."""
    due_date = datetime.now() + timedelta(days=1)
    
    schedule = schedule_manager.create_schedule(
        user_id="test_user",
        title="Test Schedule",
        description="Test description",
        due_date=due_date,
        priority="high",
        category="homework",
    )
    
    assert schedule.title == "Test Schedule"
    assert schedule.priority == "high"
    assert schedule.is_completed == False


def test_create_schedule_invalid_priority(schedule_manager):
    """Test creating a schedule with invalid priority."""
    due_date = datetime.now() + timedelta(days=1)
    
    with pytest.raises(ValueError):
        schedule_manager.create_schedule(
            user_id="test_user",
            title="Test Schedule",
            description="Test description",
            due_date=due_date,
            priority="invalid",
            category="homework",
        )


def test_get_schedule(schedule_manager):
    """Test getting a schedule."""
    due_date = datetime.now() + timedelta(days=1)
    
    created_schedule = schedule_manager.create_schedule(
        user_id="test_user",
        title="Test Schedule",
        description="Test description",
        due_date=due_date,
        priority="high",
        category="homework",
    )
    
    retrieved_schedule = schedule_manager.get_schedule(created_schedule.id)
    
    assert retrieved_schedule is not None
    assert retrieved_schedule.title == "Test Schedule"


def test_mark_completed(schedule_manager):
    """Test marking a schedule as completed."""
    due_date = datetime.now() + timedelta(days=1)
    
    schedule = schedule_manager.create_schedule(
        user_id="test_user",
        title="Test Schedule",
        description="Test description",
        due_date=due_date,
        priority="high",
        category="homework",
    )
    
    updated = schedule_manager.mark_completed(schedule.id, True)
    
    assert updated.is_completed == True
