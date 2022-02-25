from api.schemas.user import User
from fastapi import  Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update
from typing import List, Optional, Tuple

import api.models.course as course_model
import api.models.user as user_model

import api.schemas.course as course_schema

from api.db import get_db

async def update_course_name_db(db:AsyncSession, update_course_name_request: course_schema.UpdateCourseNameRequest, user:User):
    new_course_name = update_course_name_request.course_name
    author_reulst: Result = await(
        db.execute(
            select(
                course_model.Course.created_by
            ).where(course_model.Course.id == update_course_name_request.course_id)
        )
    )

    if(author_reulst.first()[0] == user.id):
        update_result: Result = await(
            db.execute(
                update(course_model.Course)
                .where(course_model.Course.id == update_course_name_request.course_id)
                .values(course_name = new_course_name)
            )
        )
        result = {"success":True, "course_name": new_course_name}
    else:
        result = {"success":False}
    await db.commit()
    return result

async def update_course_datetime_db(db:AsyncSession, update_course_datetime_request: course_schema.UpdateCourseDatetimeRequest, user:User):
    course_id = update_course_datetime_request.course_id
    new_start_date_time = update_course_datetime_request.start_date_time
    new_end_date_time = update_course_datetime_request.end_date_time
    author_reulst: Result = await(
        db.execute(
            select(
                course_model.Course.created_by
            ).where(course_model.Course.id == course_id)
        )
    )

    if(author_reulst.first()[0] == user.id):
        update_result: Result = await(
            db.execute(
                update(course_model.Course)
                .where(course_model.Course.id == course_id)
                .values(start_date_time = new_start_date_time, end_date_time = new_end_date_time)
            )
        )
        result = {"success":True, "start_date_time": new_start_date_time, "end_date_time": new_end_date_time}
    else:
        result = {"success":False}
    await db.commit()
    return result

async def insert_taking_course_student(db:AsyncSession, register_taking_course_request: course_schema.RegisterTakingCourseRequest, user:User):
    user_result: Result = await(
        db.execute(
            select(
                user_model.User.id
            ).where(user_model.User.email == register_taking_course_request.email)
        )
    )
    row = user_result.first()
    if row == None:
        return {"success": False, "error_msg": "ユーザが見つかりませんでした。"}
    user_id = row[0]
    taking_course_result: Result = await(
        db.execute(
            select(
                course_model.TakingCourse.user_id,
                course_model.TakingCourse.course_id
            ).where(course_model.TakingCourse.user_id == user_id)
            .where(course_model.TakingCourse.course_id == register_taking_course_request.course_id)
        )
    )
    if taking_course_result.first() != None:
        return {"success": False, "error_msg": "ユーザはすでにこのコースを履修中です。"}

    row = course_model.TakingCourse(course_id=register_taking_course_request.course_id, user_id=user_id)
    db.add(row)
    await db.commit()
    return {"success": True}

async def update_course_name(db:AsyncSession, update_course_name_request: course_schema.UpdateCourseNameRequest, user:User):
    course_name_response = await update_course_name_db(db=db, update_course_name_request=update_course_name_request, user=user)
    return course_name_response

async def update_datetime(db:AsyncSession, update_course_datetime_request: course_schema.UpdateCourseDatetimeRequest, user:User):
    course_datetime_response = await update_course_datetime_db(db=db, update_course_datetime_request=update_course_datetime_request, user=user)
    return course_datetime_response
    
async def register_taking_student(db:AsyncSession, register_taking_course_request: course_schema.RegisterTakingCourseRequest, user:User):
    register_taking_course_response = await insert_taking_course_student(db=db,register_taking_course_request=register_taking_course_request, user=user)
    return register_taking_course_response
