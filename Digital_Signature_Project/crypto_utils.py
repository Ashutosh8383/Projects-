from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

KEY_DIR = "keys"
os.makedirs(KEY_DIR, exist_ok=True)


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open(f"{KEY_DIR}/private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(f"{KEY_DIR}/public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def sign_document(path):
    with open(f"{KEY_DIR}/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None
        )

    with open(path, "rb") as f:
        data = f.read()

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    sig_path = path + ".sig"
    with open(sig_path, "wb") as f:
        f.write(signature)

    return sig_path


def verify_document(path):
    with open(f"{KEY_DIR}/public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    with open(path, "rb") as f:
        data = f.read()

    with open(path + ".sig", "rb") as f:
        signature = f.read()

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False