from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class FlowCreate(BaseModel):
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
