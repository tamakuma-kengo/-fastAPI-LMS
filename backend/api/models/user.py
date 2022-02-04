
# ユーザ情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME
from sqlalchemy.orm import relationship

import datetime

from api.db import Base

# ユーザ情報
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    email = Column(String(256),unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    created = Column(DATETIME,default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean,default=True, nullable=False)
    user_kind_id = Column(Integer, ForeignKey("user_kind.id"), nullable=False)

    user_kind = relationship("UserKind")

# ユーザ種別と作成権限
class UserKind(Base):
    __tablename__ = "user_kind"

    id = Column(Integer, primary_key=True,index=True)
    kind_name = Column(String(128), nullable=False, comment="ユーザの種別名")
    create = Column(Boolean,default=False, nullable=False, comment="コースやフローを作成する権限があるか.")
