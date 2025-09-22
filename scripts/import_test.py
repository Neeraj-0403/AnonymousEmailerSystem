import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).resolve().parents[1]
src_path = str(project_root / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from application.auth_service import AuthService
    from application.email_service import EmailService
    print('Imported AuthService and EmailService successfully')
except Exception as e:
    print('Import test failed:', e)
    raise
