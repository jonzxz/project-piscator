from cryptography.fernet import Fernet, InvalidToken
import os, sys

# Fernet -> AES128 in CBC with PKCS7 padding
# Fernet wrapper, used for encrypting application passwords of EmailAddress
class Encryption:
    def __init__(self):
        self.__key = os.environ.get('SECRET') or self.read_secret()
        self.__encrypter = Fernet(self.__key)

    def read_secret(self) -> str:
        try:
            with open('SECRET.key', 'r') as secret:
                key = secret.read()
                secret.close()
            return key
        except FileNotFoundError as fnfe:
            print("Secret key file not found!")
            sys.exit(1)

    def encrypt(self, plain_text: str) -> str:
        try:
            return self.get_encrypter().encrypt(bytes(plain_text, 'utf-8')).decode('utf-8')
        except TypeError as te:
            print("Plain text not a string argument!")
            return None

    def decrypt(self, cipher_text: str) -> str:
        try:
            return self.get_encrypter().decrypt(bytes(cipher_text, 'utf-8')).decode('utf-8')
        except InvalidToken as it:
            print("Cipher text not valid!")
            return None

    def get_encrypter(self) -> Fernet:
        return self.__encrypter
