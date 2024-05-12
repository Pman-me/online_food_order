from passlib.context import CryptContext


class Hash:

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @staticmethod
    def create_hash(password: str):
        return Hash.pwd_context.hash(password)

    @staticmethod
    def verify_hash(plain_password: str, hashed_password):
        return Hash.pwd_context.verify(plain_password, hashed_password)