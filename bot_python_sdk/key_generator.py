import uuid

from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

from bot_python_sdk.logger import Logger


class KeyGenerator:
    def __init__(self):
        pass

    def generate_key(self):
        Logger.info('Key Generator', 'Generating KeyPair...')
        key = PKey()
        key.generate_key(TYPE_RSA, 1024)
        key = key.to_cryptography_key()
        return self._public_key(key), self._private_key(key)

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def _public_key(key):
        return key.public_key().public_bytes(Encoding.PEM, PublicFormat.PKCS1).decode("utf-8")

    @staticmethod
    def _private_key(key):
        return key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()).decode("utf-8")
