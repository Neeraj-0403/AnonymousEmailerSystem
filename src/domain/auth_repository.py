# domain/auth_repository.py

from abc import ABC, abstractmethod
from typing import Optional
from domain.models import AuthCode

# Abstract base class for the authentication code repository.
# Defines the contract for any concrete implementation (e.g., Excel, Database).
class AuthRepository(ABC):
    @abstractmethod
    def get_auth_code(self, code: str) -> Optional[AuthCode]:
        """Retrieves an authentication code by its value."""
        pass

    @abstractmethod
    def update_auth_code_status(self, code: str, is_used: bool) -> None:
        """Updates the status of an authentication code."""
        pass
