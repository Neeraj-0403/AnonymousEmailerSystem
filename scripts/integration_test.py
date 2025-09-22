import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).resolve().parents[1]
src_path = str(project_root / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from infrastructure.encryption_service import EncryptionService
from infrastructure.excel_repository import ExcelRepository
from application.auth_service import AuthService

print('Creating EncryptionService...')
enc = EncryptionService()
print('Creating ExcelRepository...')
repo = ExcelRepository(auth_file='auth_codes_test.xlsx', email_file='emails_test.xlsx', encryption_service=enc)
print('Creating AuthService...')
service = AuthService(auth_repository=repo)
print('Integration objects created successfully')
