
# ブロック情報(コース内の要素)を示すテーブル群
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DATETIME
from sqlalchemy.orm import relationship

from api.db import Base

# ブロック情報
class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    order = Column(Integer, nullable=False, comment="コース内の表示順序. 小さい値から順に上から表示される. 同じコース内で一意.")

#ブロックの表示条件
class BlockRule(Base):
    __tablename__ = "block_rules"

    block_id = Column(Integer, ForeignKey("blocks.id"), primary_key=True)
    start_date_time = Column(DATETIME, comment="Blockの表示を開始する日時")
    end_date_time = Column(DATETIME, comment="Blockの表示を終了する日時")
    always = Column(Boolean, default=True, comment="このBlockを常に表示するか.", nullable=False)
