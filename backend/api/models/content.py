
# yamlで書かれたコンテンツを格納するテーブル
from sqlalchemy import Column, Integer, DATETIME, TEXT
from sqlalchemy.orm import relationship

from datetime import datetime

from api.db import Base

# コンテンツ情報
class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(TEXT, nullable=False, comment="yaml内のコンテンツを格納.")
    created = Column(DATETIME,default=datetime.now(), nullable=False)
