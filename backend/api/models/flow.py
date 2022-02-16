
# フロー情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME, TIME
from sqlalchemy.orm import relationship

from datetime import datetime

from api.db import Base

# フロー情報
class Flow(Base):
    __tablename__ = "flows"

    id = Column(Integer, primary_key=True, index=True)
    id_in_yml = Column(String(256), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(128), nullable=False, comment="フローの名称.")
    created = Column(DATETIME,default=datetime.now(), nullable=False)
    welcome_page_content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, comment="フローの最初に表示されるコンテンツのid.")
    completion_page_content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, comment="フローの最後に表示されるコンテンツのid.")

# フロー解答の閲覧権限情報
class FlowGrant(Base):
    __tablename__ = "flow_grant"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    flow_id = Column(Integer, ForeignKey("flows.id"), primary_key=True)
    start_date_time = Column(DATETIME, nullable=False, comment="権限が有効になる日時.")
    end_date_time = Column(DATETIME, nullable=False, comment="権限が失効する日時")
    read_answer = Column(Boolean, default=False, nullable=False, comment="読み取り権限.")
    update_answer = Column(Boolean, default=False, nullable=False, comment="更新権限.")
    delete_answer = Column(Boolean, default=False, nullable=False, comment="削除権限.")

# フローのルール情報
class FlowRule(Base):
    __tablename__ = "flow_rules"

    flow_id = Column(Integer, ForeignKey("flows.id"), primary_key=True)
    check_answer_timing = Column(String(32), default="submit_page",comment="答え合わせをするタイミング. ['None','submit_page','end_of_flow']")
    challenge_limit = Column(Integer, comment="フローに挑戦できる回数")
    restart_session = Column(Boolean, default= True, nullable= False, comment="中断したセッションをリスタートできるか否か.")
    time_limit = Column(TIME, comment="Flowの制限時間を設定する.")
    start_date_time = Column(DATETIME, comment="Flowの表示を開始する日時.")
    end_answer_date_time = Column(DATETIME, comment="Flowの表示を終了する日時.")
    end_read_date_time = Column(DATETIME, comment="Flowの閲覧を終了する日時.")
    always = Column(Boolean, default=True, comment="このFlowを常に表示するか否か.")
