import  api.schemas.user as user_schema
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
import api.models.flow as flow_model

import api.schemas.course as course_schema

from api.db import get_db

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

async def select_created_courses(db: AsyncSession, user: user_schema.User) -> List[course_schema.TakingCourseResponse]:
    result: Result = await(
        db.execute(
            select(
                course_model.Course.id.label("course_id"),
                course_model.Course.course_name,
                course_model.Course.start_date_time,
                course_model.Course.end_date_time
            ).where(course_model.Course.created_by == user.id)
        )
    )
    return result.all()

async def select_course_info(db: AsyncSession, course_id:int, user: user_schema.User) -> course_schema.CourseInfoResponse:
    result: Result = await(
        db.execute(
            select(
                course_model.Course.course_name,
                course_model.Course.created,
                course_model.Course.start_date_time,
                course_model.Course.end_date_time,
            ).where(course_model.Course.id == course_id)
            .where(course_model.Course.created_by == user.id)
        )
    )
    return result.first()

async def select_course(db: AsyncSession,course_id: int) -> course_schema.CourseResponse:
    course_result: Result = await(
        db.execute(
            select(
                course_model.Course.id.label("course_id"),
                course_model.Course.course_name,
            ).where(course_model.Course.id == course_id)
        )
    )

    block_result: Result = await(
        db.execute(
            select(
                block_model.Block.order,
                content_model.Content.content,
                block_model.BlockRule.start_date_time,
                block_model.BlockRule.end_date_time,
                block_model.BlockRule.always
            ).where(block_model.Block.course_id == course_id)
            .where(block_model.Block.content_id == content_model.Content.id)
            .where(block_model.Block.id == block_model.BlockRule.block_id)
            .order_by(block_model.Block.order)
        )
    )

    flow_result: Result = await(
        db.execute(
            select(
                flow_model.Flow.id,
                flow_model.Flow.id_in_yml,
            ).where(flow_model.Flow.course_id == course_id)
        )
    )

    course_dict = course_result.mappings().first()
    block_dict_list = block_result.mappings().all()
    flow_dict_list = flow_result.mappings().all()
    block_list = []
    flow_link_list = []
    for block_d in block_dict_list:
        rule_response = course_schema.BlockRuleResponse(
            start_date_time = block_d["start_date_time"],
            end_date_time = block_d["end_date_time"],
            always = block_d["always"],
        )

        block_list += [ 
            course_schema.BlockResponse(
            order = block_d["order"],
            content = block_d["content"],
            rule =  rule_response
        )
        ]
    for flow_d in flow_dict_list:
        flow_link_list += [
            course_schema.FlowLinkResponse(
                flow_id = flow_d["id"],
                id_in_yml = flow_d["id_in_yml"]
            )
        ]

    output_dict = {
        "course_id": course_dict["course_id"],
        "course_name": course_dict["course_name"],
        "blocks": block_list,
        "flow_links" :flow_link_list
    }
    return output_dict

async def select_taking_users(db: AsyncSession, course_id:int, user: user_schema.User) -> List[user_schema.TakingCourseUserResponse]:
    result: Result = await(
        db.execute(
            select(
                user_model.User.username,
                user_model.User.email,
                user_model.User.is_active,
                user_model.UserKind.kind_name,
            ).where(course_model.Course.created_by == user.id)
            .where(course_model.Course.id == course_id)
            .where(course_model.Course.id == course_model.TakingCourse.course_id)
            .where(user_model.User.id == course_model.TakingCourse.user_id)
            .where(user_model.User.user_kind_id == user_model.UserKind.id)
        )
    )
    return result.all()
    
async def get_taking_courses(authed_token=Depends(get_authed_token),db: AsyncSession = Depends(get_db)):
    taking_courses = await select_taking_course(db=db,email=authed_token.email)
    return taking_courses

async def get_created_courses(db:AsyncSession, creater:user_schema.User):
    return await select_created_courses(db=db, user=creater)

async def get_course_info(course_id:int, creater:user_schema.User, db:AsyncSession):
    return await select_course_info(db=db, course_id=course_id, user=creater)

async def is_course_readable(db:AsyncSession, email:str, course_id:int):
    taking_courses = await select_taking_course(db=db,email=email)
    is_taking = course_id in [course.course_id for course in taking_courses]
    return is_taking

async def get_course(db:AsyncSession, course_id:int):
    course_response = await select_course(db=db, course_id=course_id)
    return course_response

async def get_taking_users(db:AsyncSession, user:user_schema.User, course_id:int):
    taking_users_response = await select_taking_users(db=db, user=user, course_id=course_id)
    return taking_users_response

