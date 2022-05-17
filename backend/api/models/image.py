from sqlalchemy import Column, Integer, String, LargeBinary

from api.db import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(30), nullable=True, comment="画像ファイル名.")
    imgdata = Column(LargeBinary(length=(2**32)-1),nullable=True)