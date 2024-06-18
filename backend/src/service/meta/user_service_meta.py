
from abc import ABC, abstractmethod

from src.schemas.user import UserGet, UserModel

class UserServiceMeta(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> UserGet:
        """Get user by id method definition"""
        pass

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> str:
        """Get user by email method definition"""
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> UserGet:
        """Create user method definition"""
        pass

    @abstractmethod
    def update_user(self, user_id: str, updated_data: dict) -> UserGet:
        """Update user method definition"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete user method definition"""
        pass

