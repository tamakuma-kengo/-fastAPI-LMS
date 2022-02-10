from sqlalchemy import true
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Response

from api.schemas.token import Token, FormData
from api.schemas.user import User, HomeUserProfile
from api.cruds.user import get_current_active_user,authenticate_user, add_user, get_current_active_creater
from api.cruds.domains.generate_token import create_access_token
from api.db import get_db

from datetime import timedelta
from typing import Optional

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    return {"token": token}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: FormData, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db,form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.set_cookie(key="token", value = access_token, httponly=True)
    return response

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user:User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/creater/", response_model=HomeUserProfile)
async def read_users_me(current_creater:User = Depends(get_current_active_creater)):
    return current_creater

@router.get("/err")
async def read_item():
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/users/me/items/")
async def read_own_items(current_user:User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.post("/signup")
async def singup(username: str, email: str, password: str, re_password: str, db: AsyncSession = Depends(get_db)):
    if len(email) > 1 and len(password) > 1 and password==re_password:
        return await add_user(db, username, email, password)
    else:
        return HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Signup Failed")
