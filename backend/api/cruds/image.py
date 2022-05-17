import  api.schemas.user as user_schema
from fastapi import  Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select

import api.models.image as image_model

import api.schemas.image as image_schema


async def select_image(db:AsyncSession, image_id: int) -> image_schema.ImageResponse:
    result: Result = await(
        db.execute(
            select(
                image_model.Image.imgdata,
            ).where(image_model.Image.id == image_id)
        )
    )
    return result.first()

async def get_image(db:AsyncSession, image_id:int):
    image_responce = await select_image(db=db, image_id=image_id)
    image_only = image_responce[0]
    return image_only
