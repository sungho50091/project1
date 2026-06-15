"""
User account management.

Handles user registration, authentication, and profile management.
"""

from typing import Optional
from datetime import datetime
from uuid import uuid4
import hashlib

from models.user import User
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AccountManager:
    """
    Manages user accounts and authentication.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize AccountManager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_account(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        grade: Optional[int] = None,
    ) -> User:
        """
        Create a new user account.
        
        Args:
            username: Username
            email: Email address
            password: Password (will be hashed)
            name: User's full name
            grade: School grade (optional)
        
        Returns:
            Created User object
        
        Raises:
            ValueError: If validation fails or user already exists
        """
        # Validation
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        
        # Check if user already exists
        if self.db.get_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists")
        
        user = User(
            id=str(uuid4()),
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            name=name,
            grade=grade,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        logger.info(f"Creating account: {username}")
        self.db.create_user(user)
        return user
    
    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Password
        
        Returns:
            User object if authentication succeeds, None otherwise
        """
        user = self.db.get_user_by_username(username)
        if not user:
            logger.warning(f"Authentication failed: user {username} not found")
            return None
        
        if not self._verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: invalid password for {username}")
            return None
        
        logger.info(f"User authenticated: {username}")
        return user
    
    def update_profile(
        self,
        user_id: str,
        **kwargs,
    ) -> User:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
        
        Returns:
            Updated User object
        """
        user = self.db.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        logger.info(f"Updating profile: {user_id}")
        return self.db.update_user(user_id, **kwargs)
    
    def change_password(
        self,
        user_id: str,
        old_password: str,
        new_password: str,
    ) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
        
        Returns:
            True if password changed successfully
        
        Raises:
            ValueError: If old password is incorrect
        """
        user = self.db.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if not self._verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")
        
        new_hash = self._hash_password(new_password)
        self.db.update_user(user_id, password_hash=new_hash)
        logger.info(f"Password changed for user: {user_id}")
        return True
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password
            password_hash: Stored hash
        
        Returns:
            True if password matches hash
        """
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
