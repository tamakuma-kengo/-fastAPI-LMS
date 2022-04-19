import io
from os import isatty
from typing import List,Optional
from urllib import response
from api.cruds.user import get_current_active_creater, get_user_grant
from api.schemas.user import User, UserWithGrant
from api.cruds.user import get_current_active_user
from api.schemas.user import HomeUserProfile

from fastapi import APIRouter,Depends,HTTPException,status,Response
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import api.schemas.course as course_schema
import api.schemas.user as user_schema
import api.schemas.image as image_schema
import api.models.course as course_model
import api.cruds.create_course as create_course_crud
import api.cruds.read_course as read_course_crud
import api.cruds.image as image_crud
import api.cruds.update_course as update_course_crud



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

@router.get("/get_course_info/{course_id}", response_model=course_schema.CourseInfoResponse)
async def get_course_info(course_id:int, creater:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await read_course_crud.get_course_info(course_id=course_id,creater=creater, db=db)

@router.get("/get_created_courses", response_model=List[course_schema.TakingCourseResponse])
async def get_created_courses(creater:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await read_course_crud.get_created_courses(creater=creater, db=db)

@router.get("/get_course/{course_id}", response_model=course_schema.CourseResponse)
async def get_course(course_id:int, user:User=Depends(get_current_active_user),db:AsyncSession=Depends(get_db)):
    assert(user != None)
    is_readable = await read_course_crud.is_course_readable(db=db, email=user.email, course_id=course_id)
    if is_readable:
        course_respose = await read_course_crud.get_course(db=db, course_id=course_id)
        return course_respose
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

@router.post("/update_course_name", response_model=course_schema.UpdateCourseNameResponse)
async def update_course_name(update_course_name_request: course_schema.UpdateCourseNameRequest,user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        return await update_course_crud.update_course_name(db=db, user=user,update_course_name_request=update_course_name_request)

@router.post("/update_date_time", response_model=course_schema.UpdateCourseDatetimeResponse)
async def update_course_name(update_course_datetime_request: course_schema.UpdateCourseDatetimeRequest,user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        return await update_course_crud.update_datetime(db=db, user=user,update_course_datetime_request=update_course_datetime_request)

@router.get("/get_taking_students/{course_id}", response_model=List[user_schema.TakingCourseUserResponse])
async def get_course_taking(course_id:int, user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        return await read_course_crud.get_taking_users(db=db, user=user, course_id=course_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

@router.post("/register_taking_student/", response_model=course_schema.RegisterTakingCourseResponse)
async def register_taking_student(register_taking_course_request: course_schema.RegisterTakingCourseRequest, user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await update_course_crud.register_taking_student(db=db, user=user, register_taking_course_request=register_taking_course_request)

"""
@router.get("/get_image/{image_id}", response_model=image_schema.ImageResponse)
async def get_image(image_id:int, user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        return await image_crud.get_image(db=db, image_id=image_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")


@router.get("/get_image/{image_id}")
async def get_image(image_id:int):
    image1 = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\n\x00\x00\x00\n\x08\x02\x00\x00\x00\x02PX\xea\x00\x00\x00cIDATx\x9c}\xce\xb1\r\xc0 \x0c\x04@\x87\xca%%\xa5\xbd\x19%[0\nl\x01\xdb}\n#\x82\x08\xc9\x97\x7f\x96\xf5\x17\x00\xfa\x8e\xfb\xb1\x9d{\xef\xaa\xaa\xaa\xb5\xd6Q\x01\x00\xd0Z\x13\x91y\xc7\xcc\xd6\x93\x99\xf7~}\x93Rz8\x84p\xb4\xc1G8\xb0\x88\x94Rvf\xe6\xf7(\x8b#\xa2\x9c\xf3\xe4\x18\xe3\xba\xe3\x06U,fny:h\x00\x00\x00\x00\x00IEND\xaeB`\x82'
    image_stream = io.BytesIO(image1)
    return StreamingResponse(content=image_stream, media_type="image/png")
"""

@router.get("/get_image/{image_id}", response_model=image_schema.ImageResponse)
async def get_image(image_id:int, user:User=Depends(get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        image_stream = io.BytesIO(await image_crud.get_image(db=db, image_id=image_id))
        return StreamingResponse(content=image_stream, media_type="image/png")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
