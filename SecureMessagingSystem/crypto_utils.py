from cryptography.fernet import Fernet
import os
import hmac
import hashlib

KEY_FILE = "data/secret.key"

def generate_key():

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE,"wb") as f:
            f.write(key)

def load_key():

    with open(KEY_FILE,"rb") as f:
        return f.read()

generate_key()

cipher = Fernet(load_key())

def encrypt_message(message):

    encrypted = cipher.encrypt(
        message.encode()
    )

    return encrypted.decode()

def decrypt_message(message):

    return cipher.decrypt(
        message.encode()
    ).decode()

def create_hmac(message):

    key = load_key()

    return hmac.new(
        key,
        message.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_hmac(message,hmac_value):

    generated = create_hmac(message)

    return hmac.compare_digest(
        generated,
        hmac_value
    )