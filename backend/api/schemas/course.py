from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

# ユーザ登録時のレスポンス
class AddedUsers(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    created: datetime
    is_active: bool
    user_kind_id: int

class AddUsersResponse(BaseModel):
    success: bool
    error_msg: str
    added_users: Optional[AddedUsers] = None

# ユーザ登録時のリクエスト
class AddUsersRequest(BaseModel):
    username: str
    email: str
    password: str
    kind_id: int

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

# コース更新時のリクエスト
class UpdateCourseNameRequest(BaseModel):
    course_id: int
    course_name: str

class UpdateCourseDatetimeRequest(BaseModel):
    course_id: int
    start_date_time: datetime
    end_date_time: datetime

# コース更新時のレスポンス
class UpdateCourseNameResponse(BaseModel):
    success: bool
    course_name: Optional[str] = None

class UpdateCourseDatetimeResponse(BaseModel):
    success: bool
    start_date_time: Optional[datetime] = None
    end_date_time: Optional[datetime] = None

# 履修者登録時のリクエスト
class RegisterTakingCourseRequest(BaseModel):
    course_id: int
    email: str

# 履修者登録時のレスポンス
class RegisterTakingCourseResponse(BaseModel):
    success: bool
    error_msg: Optional[str] = None

## insert用のスキーマ群
class CourseCreate(BaseModel):
    course_name: str
    start_date_time: datetime
    end_date_time:datetime
    created_by: int

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

class CourseInfoResponse(BaseModel):
    course_name: str
    created: datetime
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

class FlowLinkResponse(BaseModel):
    flow_id: int
    id_in_yml: str

class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    blocks: List[BlockResponse]
    flow_links: List[FlowLinkResponse]

# コース情報（シラバス情報）を取得するレスポンス
class CourseInfoSyllabusResponse(BaseModel):
    course_id: int
    subject_class: str
    subject_name: str
    subject_credit: int
    subject_code: str
    subject_period: str


# コース情報を登録するスキーマ
class CourseInfoSyllabusCreate(BaseModel):
    course_id: int
    subject_class: str
    subject_name: str
    subject_credit: int
    subject_code: str
    subject_period: str