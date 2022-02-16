from os import isatty
from typing import List,Optional
from urllib import response
from api.cruds.user import get_user_grant
from api.schemas.user import UserWithGrant
from api.cruds.user import get_current_active_user
from api.schemas.user import HomeUserProfile

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import api.schemas.course as course_schema
import api.cruds.create_course as create_course_crud
import api.cruds.read_course as read_course_crud

from api.db import get_db

router = APIRouter()

@router.post("/register_course", response_model=course_schema.RegisterCourseResponse)
async def register_course(register_course_request: course_schema.RegisterCourseRequest,user_grant:UserWithGrant=Depends(get_user_grant),db:AsyncSession=Depends(get_db)):
    if not user_grant.create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return  await create_course_crud.register_course(user_grant,register_course_request,db)

@router.get("/get_courses", response_model=List[course_schema.TakingCourseResponse])
async def get_taking_courses(taking_courses:List[course_schema.TakingCourseResponse]=Depends(read_course_crud.get_taking_courses)):
    return taking_courses

@router.get("/get_course/{course_id}", response_model=course_schema.CourseResponse)
async def get_course(course_id:int, user:HomeUserProfile=Depends(get_current_active_user),db:AsyncSession=Depends(get_db)):
    assert(user != None)
    is_readable = await read_course_crud.is_course_readable(db=db, email=user.email, course_id=course_id)
    if is_readable:
        course_respose = await read_course_crud.get_course(db=db, course_id=course_id)
        return course_respose
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
