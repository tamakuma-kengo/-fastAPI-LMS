from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

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

