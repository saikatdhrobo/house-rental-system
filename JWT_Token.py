
from fastapi.responses import JSONResponse
from fastapi import status

from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError

from SECRET_DATA import JWT_Info


SECRET_KEY = JWT_Info.secret_key()
ALGORITHM = JWT_Info.algo()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': 'unauthorized'})
        
    except InvalidTokenError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': 'unauthorized'})
    
    return user_id
