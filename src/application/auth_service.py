# application/auth_service.py

from domain.auth_repository import AuthRepository
from infrastructure.logger import logger

class AuthService:
    """
    Application service for handling authentication-related use cases.
    It orchestrates the domain and infrastructure layers for authentication logic.
    """
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def validate_and_use_code(self, code: str) -> bool:
        """
        Validates an authentication code and marks it as used if valid.
        
        Args:
            code (str): The one-time code entered by the user.
            
        Returns:
            bool: True if the code is valid and was successfully marked as used, False otherwise.
        """
        try:
            # Get the code from the repository
            auth_code = self.auth_repository.get_auth_code(code)
            
            if auth_code:
                # If the code exists and is not used, update its status
                self.auth_repository.update_auth_code_status(code, True)
                logger.info(f"Code '{code}' validated and marked as used.")
                return True
            else:
                logger.warning(f"Invalid or already used code '{code}'.")
                return False
        except Exception as e:
            logger.error(f"Error validating code: {e}")
            return False
