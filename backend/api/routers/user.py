from sqlalchemy import true
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Response

from api.schemas.token import Token
from api.schemas.user import HomeUserProfile

from api.db import get_db
from api.cruds.user import get_home_profile

from datetime import timedelta
from typing import Optional

router = APIRouter()

@router.get("/home_profile/",response_model=HomeUserProfile)
async def get_home_user_profile(user_profile=Depends(get_home_profile)):
    return user_profile
