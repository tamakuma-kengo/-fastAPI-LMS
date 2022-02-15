from fastapi import  Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Cookie, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert
from typing import List, Optional, Tuple
from jose import JWTError, jwt
from datetime import datetime

from api.schemas.user import HomeUserProfile, User, UserCreate, UserWithGrant
import api.models.user as user_model
import api.schemas.user as user_schema
from api.cruds.domains.generate_hash import verify_password,get_password_hash
from api.schemas.token import TokenData
from api.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

async def get_user(db: AsyncSession,email: str) -> List[user_schema.User]:
    result: Result = await(
        db.execute(
            select(
                user_model.User.id,
                user_model.User.username,
                user_model.User.email,
                user_model.User.hashed_password,
                user_model.User.created,
                user_model.User.is_active,
                user_model.User.user_kind_id
            ).where(user_model.User.email == email)
        )
    )
    return result.first()

async def get_user_profile(db: AsyncSession,email: str) -> List[user_schema.HomeUserProfile]:
    result: Result = await(
        db.execute(
            select(
                user_model.User.username,
                user_model.User.email,
                user_model.User.is_active,
                user_model.UserKind.kind_name,
                user_model.UserKind.create
            ).where(user_model.User.email == email)
            .where(user_model.User.user_kind_id == user_model.UserKind.id)
        )
    )
    # print(result.all())
    return result.first()

async def select_user_with_grant(db: AsyncSession,email: str) -> List[user_schema.UserWithGrant]:
    result: Result = await(
        db.execute(
            select(
                user_model.User.id,
                user_model.User.username,
                user_model.User.email,
                user_model.User.created,
                user_model.User.is_active,
                user_model.UserKind.kind_name,
                user_model.UserKind.create
            ).where(user_model.User.email == email)
            .where(user_model.User.user_kind_id == user_model.UserKind.id)
        )
    )
    # print(result.all())
    return result.first()


async def add_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = UserCreate(username = username, email = email, hashed_password = hashed_password, created = datetime.now(), is_active = True)
    row = user_model.User(**new_user.dict())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return "success"

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_token(token: Optional[str] = Cookie(None)):
    return token

async def get_authed_token(token=Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception

async def get_current_user(db: AsyncSession = Depends(get_db),token: Optional[str] = Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception
    user = await get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
    

async def get_current_active_user(current_user:User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



async def get_home_profile(db: AsyncSession = Depends(get_db),token: Optional[str] = Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception
    user_profile = await get_user_profile(db, email=token_data.email)
    if user_profile is None:
        raise credentials_exception
    return user_profile

async def get_user_with_grant(db: AsyncSession = Depends(get_db),token: Optional[str] = Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token == None:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception
    user_with_grant = await select_user_with_grant(db, email=token_data.email)
    if user_with_grant is None:
        raise credentials_exception
    return user_with_grant

async def get_current_active_creater(currenct_creater:HomeUserProfile = Depends(get_home_profile)):
    if not currenct_creater.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not currenct_creater.create:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currenct_creater

async def get_user_grant(current_user:UserWithGrant = Depends(get_user_with_grant)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not current_user.create:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

