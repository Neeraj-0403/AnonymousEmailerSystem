import pandas as pd
import random

# Generate 10 random 6-digit MFA codes
mfa_codes = []
for _ in range(10):
    code = str(random.randint(100000, 999999))
    mfa_codes.append(code)

# Create DataFrame
df = pd.DataFrame({
    'code': mfa_codes,
    'is_used': [False] * len(mfa_codes)
})

# Save to Excel
df.to_excel('auth_codes.xlsx', index=False)

print("Generated MFA codes:")
for code in mfa_codes:
    print(f"- {code}")