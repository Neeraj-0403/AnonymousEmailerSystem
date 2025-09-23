import pyotp

# Read the secret
with open('totp_secret.txt', 'r') as f:
    secret = f.read().strip()

# Create TOTP object
totp = pyotp.TOTP(secret)

# Get current code
current_code = totp.now()
print(f"Current TOTP code: {current_code}")

# Test validation
test_codes = [current_code, "020684"]
for code in test_codes:
    is_valid = totp.verify(code, valid_window=1)
    print(f"Code {code}: {'Valid' if is_valid else 'Invalid'}")