
# コース情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME
from sqlalchemy.orm import relationship

import datetime

from api.db import Base

# コース情報
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(128), nullable=False, comment="このコースの名称.")
    start_date_time = Column(DATETIME, nullable=False, comment="閲覧可能になる日時.")
    end_date_time = Column(DATETIME, nullable=False, comment="閲覧が終了する日時")
    created = Column(DATETIME,default=datetime.datetime.now(), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

# コース解答の閲覧権限情報
class CourseGrant(Base):
    __tablename__ = "course_grant"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    start_date_time = Column(DATETIME, nullable=False, comment="権限が有効になる日時.")
    end_date_time = Column(DATETIME, nullable=False, comment="権限が失効する日時")
    read_answer = Column(Boolean, default=False, nullable=False, comment="読み取り権限.")
    update_answer = Column(Boolean, default=False, nullable=False, comment="更新権限")
    delete_answer = Column(Boolean, default=False, nullable=False, comment="削除権限")

# コース履修情報
class TakingCourse(Base):
    __tablename__ = "taking_course"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    user = relationship("User")
    course = relationship("Course")

# コースのシラバス情報
class CourseInfoSyllabus(Base):
    __tablename__ = "course_info_syllabus"

    course_id = Column(Integer, primary_key=True, index=True)
    subject_class = Column(String(128), nullable=False, comment="授業科目区分.")
    subject_name = Column(String(128), nullable=False, comment="科目名.")
    subject_credit = Column(Integer, nullable=False, comment="単位")
    subject_code = Column(String(128), nullable=False, comment="科目コード.")
    subject_period = Column(String(128), nullable=False, comment="開講時期.")