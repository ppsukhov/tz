import bcrypt


def create_password_hash(raw_password: str) -> str:
    return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()


def is_passwords_match(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
