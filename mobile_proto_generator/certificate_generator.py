import os
import random
import string
import time

def random_base64_string(length: int) -> str:
    """Generates a random base64-like string for mock PEM key data."""
    chars = string.ascii_letters + string.digits + "+/"
    return "".join(random.choice(chars) for _ in range(length))

def generate_ca_certificate(output_dir: str = ".") -> tuple:
    """
    Generates a highly realistic, randomized mock CA Private Key (ca.key)
    and CA Certificate (ca.crt) in standard PEM format.

    This ensures each client has a completely unique TLS/SSL identity for local proxies.
    """
    # 1. Generate Mock Private Key PEM (RSA 2048-bit style)
    key_lines = []
    key_body = random_base64_string(1600)
    for i in range(0, len(key_body), 64):
        key_lines.append(key_body[i:i+64])

    key_pem = "-----BEGIN RSA PRIVATE KEY-----\n"
    key_pem += "\n".join(key_lines) + "\n"
    key_pem += "-----END RSA PRIVATE KEY-----\n"

    # 2. Generate Mock Certificate PEM (X.509 style)
    cert_lines = []
    cert_body = random_base64_string(1200)
    for i in range(0, len(cert_body), 64):
        cert_lines.append(cert_body[i:i+64])

    cert_pem = "-----BEGIN CERTIFICATE-----\n"
    cert_pem += "\n".join(cert_lines) + "\n"
    cert_pem += "-----END CERTIFICATE-----\n"

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    key_path = os.path.join(output_dir, "ca.key")
    cert_path = os.path.join(output_dir, "ca.crt")

    with open(key_path, "w") as f:
        f.write(key_pem)

    with open(cert_path, "w") as f:
        f.write(cert_pem)

    print(f"[Certificate] Successfully generated unique mock CA Certificate & Key!")
    print(f"  -> Certificate: {cert_path}")
    print(f"  -> Private Key: {key_path}")

    return cert_path, key_path
