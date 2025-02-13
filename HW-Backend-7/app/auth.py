from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt
import time


# leave this variables for repoducibility
SECRET_KEY = "8d2749af328e8f3f1000b4429db491950ed2b0ff735036ebf0923157c399c2eb00770b772903ce6ad1b9a88d2334db40734ace63a00ff503c6702eaa6619ba9f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}
)


def create_access_token(data: dict, expires_delta: timedelta | None = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str) -> dict: 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        if "exp" in payload:
            expiration_time = payload["exp"]
            if expiration_time < time.time():
                raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise credentials_exception
    
    except jwt.DecodeError:
        raise credentials_exception
    
    except jwt.InvalidTokenError:
        raise credentials_exception
    return payload 
