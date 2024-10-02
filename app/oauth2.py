import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#Secret key
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data):
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return access_token


def verify_token(token: str, credentials_exception):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    except PyJWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail=f"Could not validate credentials", headers={"www-Authenticate":"Bearer"})
    
    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user