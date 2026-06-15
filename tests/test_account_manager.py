"""
Tests for AccountManager.
"""

import pytest

from core.account_manager import AccountManager
from database.db_manager import DatabaseManager


@pytest.fixture
def db_manager():
    """Create in-memory database for testing."""
    return DatabaseManager(":memory:")


@pytest.fixture
def account_manager(db_manager):
    """Create account manager with test database."""
    return AccountManager(db_manager)


def test_create_account(account_manager):
    """Test creating a user account."""
    user = account_manager.create_account(
        username="testuser",
        email="test@example.com",
        password="password123",
        name="Test User",
        grade=10,
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.grade == 10


def test_create_account_short_username(account_manager):
    """Test creating account with short username."""
    with pytest.raises(ValueError):
        account_manager.create_account(
            username="ab",
            email="test@example.com",
            password="password123",
            name="Test User",
        )


def test_authenticate(account_manager):
    """Test user authentication."""
    account_manager.create_account(
        username="testuser",
        email="test@example.com",
        password="password123",
        name="Test User",
    )
    
    authenticated_user = account_manager.authenticate("testuser", "password123")
    
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"


def test_authenticate_invalid_password(account_manager):
    """Test authentication with invalid password."""
    account_manager.create_account(
        username="testuser",
        email="test@example.com",
        password="password123",
        name="Test User",
    )
    
    authenticated_user = account_manager.authenticate("testuser", "wrongpassword")
    
    assert authenticated_user is None
