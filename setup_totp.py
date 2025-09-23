import pyotp
import qrcode
import pandas as pd

# Generate a secret key for TOTP
secret = pyotp.random_base32()
print(f"Secret Key: {secret}")

# Create TOTP object
totp = pyotp.TOTP(secret)

# Generate QR code for authenticator app
provisioning_uri = totp.provisioning_uri(
    name="Anonymous Portal",
    issuer_name="Mystery Messenger"
)

# Generate QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(provisioning_uri)
qr.make(fit=True)

# Save QR code
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_code.png")

print(f"QR Code saved as 'qr_code.png'")
print(f"Manual entry key: {secret}")
print(f"Current TOTP code: {totp.now()}")

# Save secret to file for backend use
with open('totp_secret.txt', 'w') as f:
    f.write(secret)