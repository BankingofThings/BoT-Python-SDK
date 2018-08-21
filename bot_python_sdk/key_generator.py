import uuid

from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption


class KeyGenerator:
    def __init__(self):
        self.key = None

    def generate_key(self):
        key = PKey()
        key.generate_key(TYPE_RSA, 1024)
        self.key = key.to_cryptography_key()

    def public_key(self):
        return self.key.public_key().public_bytes(Encoding.PEM, PublicFormat.PKCS1).decode("utf-8")

    def private_key(self):
        return self.key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()).decode("utf-8")

    def generate_uuid(self):
        return uuid.uuid4()
