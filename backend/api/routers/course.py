from typing import List,Optional
from api.cruds.user import get_user_grant
from api.schemas.user import UserWithGrant

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import api.schemas.course as course_schema
import api.cruds.course as course_crud
from api.db import get_db

router = APIRouter()

@router.post("/register_course",response_model=course_schema.RegisterCourseResponse)
async def register_course(register_course_request: course_schema.RegisterCourseRequest,user_grant:UserWithGrant=Depends(get_user_grant),db:AsyncSession=Depends(get_db)):
    if not user_grant.create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return  await course_crud.register_course(user_grant,register_course_request,db)
