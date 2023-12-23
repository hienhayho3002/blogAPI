from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from .schemas import TokenData, db


load_dotenv()

router = APIRouter(
    prefix="/get_current_user",
    tags=["User Routes"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(payload: Dict):
    to_encode = payload.copy()

    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expiration_time})

    access_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return access_token

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")

        if not id:
            raise credential_exception

        token_data = TokenData(id=id)
        return token_data

    except JWTError:
        raise credential_exception


@router.get("")
async def get_current_user(token: str = Depends(dependency=oauth2_scheme)):
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Access token not be verified",
        headers={"WWW-Authenticate": "Bearer"}
    )
    current_user_id = verify_access_token(token, credential_exception).id
    
    current_user = await db["users"].find_one(filter={"_id": current_user_id})

    return current_user

    