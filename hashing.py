from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def get_hashed_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_passowrd, hashed_password):
    return pwd_context.verify(plain_passowrd, hashed_password) #check the passwrod
