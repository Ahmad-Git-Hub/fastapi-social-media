from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_passwords(provided_password: str, hashed_password: str):
    return pwd_context.verify(provided_password, hashed_password)

