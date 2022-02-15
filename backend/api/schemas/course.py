from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime


# コース登録時のレスポンス
class RegisteredCourse(BaseModel):
    id: int
    course_name: str
    start_date_time: datetime
    end_date_time: datetime
    created: datetime

class RegisterCourseResponse(BaseModel):
    success: bool
    error_msg: str
    registered_course: Optional[RegisteredCourse] = None

# コース登録時のリクエスト
class CourseFiles(BaseModel):
    file_path: str
    file_text: str

class RegisterCourseRequest(BaseModel):
    course_name: str
    start_date_time: datetime
    end_date_time: datetime
    course_files: List[CourseFiles]


## insert用のスキーマ群
class CourseCreate(BaseModel):
    course_name: str
    start_date_time: datetime
    end_date_time:datetime

class CourseGrantCreate(BaseModel):
    user_id: int
    course_id: int
    start_date_time: datetime
    end_date_time: datetime
    read_answer: bool
    update_answer: bool
    delete_answer: bool

class BlockCreate(BaseModel):
    course_id: int
    content_id: int
    order: int

class BlockRuleCreate(BaseModel):
    block_id: int
    start_date_time: Optional[datetime]
    end_date_time: Optional[datetime]
    always:Optional[bool] = True 

# コース一覧を取得するためのレスポンス
class TakingCourseResponse(BaseModel):
    course_id: int
    course_name: str
    start_date_time: datetime
    end_date_time: datetime

# コース画面を取得するためのレスポンス
class BlockRuleResponse(BaseModel):
    start_date_time: Optional[datetime]
    end_date_time: Optional[datetime]
    always: bool

class BlockResponse(BaseModel):
    order: int
    content: str
    rule: BlockRuleResponse

class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    blocks: List[BlockResponse]
