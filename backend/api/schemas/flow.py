from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

# insert用
class FlowCreate(BaseModel):
    id_in_yml :str
    course_id: int
    title: str
    welcome_page_content_id: int
    completion_page_content_id: int

class FlowGrantCreate(BaseModel):
    user_id: int
    flow_id: int
    start_date_time: datetime
    end_date_time: datetime
    read_answer: bool
    update_answer: bool
    delete_answer: bool

class FlowRuleCreate(BaseModel):
    flow_id: int
    check_answer_timing: Optional[str]
    challenge_limit: Optional[int]
    restart_session: Optional[bool]
    start_date_time: Optional[datetime]
    end_answer_date_time: Optional[datetime]
    end_read_date_time: Optional[datetime]
    check_answer_timing: Optional[datetime]
    always: Optional[bool]

class FlowSessionCreate(BaseModel):
    user_id: int
    flow_id: int
    start_date_time: datetime

class FlowSessionBlankAnswerCreate(BaseModel):
    flow_session_id: int
    flowpage_id: int
    blank_id: str
    answer: str
    created: datetime

# レスポンス用
class FlowResponse(BaseModel):
    title: str
    check_answer_timing: str
    challenge_limit: Optional[int]
    restart_session: Optional[bool]
    time_limit: Optional[int]
    start_date_time: Optional[datetime]
    end_answer_date_time: Optional[datetime]
    end_read_date_time: Optional[datetime]
    always: bool

class FlowIdResponse(BaseModel):
    flow_id: int
    course_id: int

class FlowInfoResponse(BaseModel):
    flow_title: str
    num_of_pages: int

class FlowSessionResponse(BaseModel):
    id: int
    start_date_time: datetime
    finish_date_time: Optional[datetime]
    is_finished: bool

class StartFlowSessionResonse(BaseModel):
    start_success: bool
    flow_session_id: Optional[int]
    start_date_time: Optional[datetime]

class FinishFlowSessionResonse(BaseModel):
    finish_success: bool
    finish_date_time: Optional[datetime]

class ContentResponse(BaseModel):
    content: str

# リクエスト用
class StartFlowSessionRequest(BaseModel):
    flow_id: int

class FinishFlowSessionRequest(BaseModel):
    flow_session_id: int
