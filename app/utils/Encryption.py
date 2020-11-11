from cryptography.fernet import Fernet

class Encryption():
    def __init__(self):
        self.__key = self.read_secret()
        self.__encrypter = Fernet(self.__key)

    def read_secret(self):
        try:
            with open('SECRET.key', 'r') as secret:
                key = secret.read()
                secret.close()
            return key
        except FileNotFoundError:
            print("Secret key file not found!")
            return None

    def encrypt(self, plain_text):
        return self.get_encrypter().encrypt(bytes(plain_text, 'utf-8')).decode('utf-8')

    def decrypt(self, cipher_text):
        return self.get_encrypter().decrypt(bytes(cipher_text, 'utf-8')).decode('utf-8')

    def get_encrypter(self):
        return self.__encrypter
