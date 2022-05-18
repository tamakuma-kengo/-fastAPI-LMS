from sqlalchemy import create_engine
from fastapi import Depends
from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.orm import sessionmaker

from api.models.user import Base as UserBase, User
from api.models.content import Base as ContentBase
from api.models.course import Base as CourseBase
from api.models.block import Base as BlockBase
from api.models.flow import Base as FlowBase
from api.models.page_group import Base as PageGroupBase
from api.models.flow_page import Base as PageBase
from api.models.flow_session import Base as FlowSessionBase
from api.models.image import Base as ImageBase

from api.migration.add_rows import add_rows

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    UserBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
    ContentBase.metadata.drop_all(bind=engine)
    ContentBase.metadata.create_all(bind=engine)
    CourseBase.metadata.drop_all(bind=engine)
    CourseBase.metadata.create_all(bind=engine)
    BlockBase.metadata.drop_all(bind=engine)
    BlockBase.metadata.create_all(bind=engine)
    FlowBase.metadata.drop_all(bind=engine)
    FlowBase.metadata.create_all(bind=engine)
    PageGroupBase.metadata.drop_all(bind=engine)
    PageGroupBase.metadata.create_all(bind=engine)
    PageBase.metadata.drop_all(bind=engine)
    PageBase.metadata.create_all(bind=engine)
    FlowSessionBase.metadata.drop_all(bind=engine)
    FlowSessionBase.metadata.create_all(bind=engine)
    ImageBase.metadata.drop_all(bind=engine)
    ImageBase.metadata.create_all(bind=engine)

def drop_database():
    UserBase.metadata.drop_all(bind=engine)
    ContentBase.metadata.drop_all(bind=engine)
    CourseBase.metadata.drop_all(bind=engine)
    BlockBase.metadata.drop_all(bind=engine)
    FlowBase.metadata.drop_all(bind=engine)
    PageGroupBase.metadata.drop_all(bind=engine)
    PageBase.metadata.drop_all(bind=engine)
    FlowSessionBase.metadata.drop_all(bind=engine)
    ImageBase.metadata.drop_all(bind=engine)

def get_session():
    SessionClass = sessionmaker(engine)
    return SessionClass()

if __name__ == "__main__":
    # drop_database()
    reset_database()
    db_session = get_session()
    add_rows(db_session)
    