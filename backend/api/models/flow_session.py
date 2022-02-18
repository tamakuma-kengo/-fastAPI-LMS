
# フローセッション(フローを利用する一連の流れ)を示すテーブル群
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DATETIME, TEXT, String
from sqlalchemy.orm import relationship

from datetime import datetime

from api.db import Base

# フローセッション情報
class FlowSession(Base):
    __tablename__ = "flow_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)
    start_date_time = Column(DATETIME, comment="セッションを開始した日時.")
    finish_date_time = Column(DATETIME, comment="セッションを終了した日時.")
    is_finished = Column(Boolean, default=False, comment="セッションを終了したか否か")

# フローセッションが持つ問題情報
class FlowSessionFlowPage(Base):
    __tablename__ = "flow_session_flow_pages"

    flow_session_id = Column(Integer, ForeignKey("flow_sessions.id"), primary_key=True)
    flowpage_id = Column(Integer, ForeignKey("flowpages.id"), primary_key=True)
    order = Column(Integer, nullable=False, comment="フロー内での表示順序. 同じフロー内で一意.")
    submitted = Column(Boolean, default=False, comment="問題を解答したか否か.")

# フローセッションと各ページの解答情報
class FlowSessionBlankAnswer(Base):
    __tablename__ = "flow_session_blank_answer"

    id = Column(Integer, primary_key=True, index=True)
    flow_session_id = Column(Integer, ForeignKey("flow_sessions.id"), nullable=False)
    flowpage_id = Column(Integer, ForeignKey("flowpages.id"), nullable=False)
    blank_id = Column(String(256), ForeignKey("blanks.id"), nullable=False)
    answer = Column(TEXT, comment="ユーザが回答した内容. ")
    created = Column(DATETIME,default=datetime.now(), nullable=False, comment="回答日時")
    