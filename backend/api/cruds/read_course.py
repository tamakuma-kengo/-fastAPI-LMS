from fastapi import  Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert
from typing import List, Optional, Tuple

from api.cruds.user import get_authed_token
from api.schemas.token import TokenData
import api.models.course as course_model
import api.models.user as user_model
import api.models.block as block_model
import api.models.content as content_model

import api.schemas.course as course_schema

from api.db import get_db

from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

async def select_taking_course(db: AsyncSession,email: str) -> List[course_schema.TakingCourseResponse]:
    result: Result = await(
        db.execute(
            select(
                course_model.Course.id.label("course_id"),
                course_model.Course.course_name,
                course_model.Course.start_date_time,
                course_model.Course.end_date_time
            ).where(user_model.User.email == email)
            .where(course_model.Course.id == course_model.TakingCourse.course_id)
            .where(course_model.TakingCourse.user_id == user_model.User.id)
        )
    )
    return result.all()

async def select_course(db: AsyncSession,course_id: int) -> course_schema.CourseResponse:
    result: Result = await(
        db.execute(
            select(
                course_model.Course.id.label("course_id"),
                course_model.Course.course_name,
                block_model.Block.order,
                content_model.Content.content,
                block_model.BlockRule.start_date_time,
                block_model.BlockRule.end_date_time,
                block_model.BlockRule.always
            ).where(course_model.Course.id == course_id)
            .where(course_model.Course.id == block_model.Block.course_id)
            .where(block_model.Block.content_id == content_model.Content.id)
            .where(block_model.Block.id == block_model.BlockRule.block_id)
        )
    )
    return result.all()
    
async def get_taking_courses(authed_token=Depends(get_authed_token),db: AsyncSession = Depends(get_db)):
    taking_courses = await select_taking_course(db=db,email=authed_token.email)
    return taking_courses

async def is_course_readable(db:AsyncSession, email:str, course_id:int):
    taking_courses = await select_taking_course(db=db,email=email)
    is_taking = course_id in [course.course_id for course in taking_courses]
    return is_taking

async def get_course(db:AsyncSession, course_id:int):
    course_response = await select_course(db=db, course_id=course_id)
    return course_response