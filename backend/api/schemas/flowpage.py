from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class BlankCreate(BaseModel):
    id: str
    flowpage_id: int

class CorrectAnswerCreate(BaseModel):
    flowpage_id: int
    blank_id: str
    type: str
    value: str

# 拡張用の基底クラス
class FlowPageCreate(BaseModel):
    title: str
    content_id: int
    page_type: str

class PageCreate(FlowPageCreate):
    page_type: str = "Page"

# 拡張用の基底クラス
class QuestionCreate(FlowPageCreate):
    page_type: str = "Question"

class SingleTextQuestionCreate(QuestionCreate):
    page_type: str = "SingleTextQuestion"

class MultipleTextQuestionCreate(QuestionCreate):
    page_type: str = "MultipleTextQuestion"
    answer_column_content_id: int

class DescriptiveTextQuestionCreate(QuestionCreate):
    page_type: str = "DescriptiveTextQuestion"

class ChoiceQuestionCreate(QuestionCreate):
    page_type: str = "ChoiceQuestion"

class ChoiceQuestionChoicesCreate(BaseModel):
    id: str
    flowpage_id: int
    order: int
    content_id: int

# Response用
class ChoiceQuestionChoiceResponse(BaseModel):
    id: str
    content: str
    order: int

class FlowPageContentResponse(BaseModel):
    content: str

class PageResponse(FlowPageContentResponse):
    pass

class QuestionResponse(FlowPageContentResponse):
    pass

class SingleTextQuestionResponse(FlowPageContentResponse):
    blank_id: str

class MultipleTextQuestionResponse(FlowPageContentResponse):
    answer_column_content: str

class DescriptiveTextQuestionResponse(FlowPageContentResponse):
    blank_id: str

class ChoiceQuestionResponse(FlowPageContentResponse):
    choices : List[ChoiceQuestionChoiceResponse]
    blank_id: str

class FlowpageResponse(BaseModel):
    title: str
    page_type: str
    page_content: FlowPageContentResponse

class BlankAnswerResponse(BaseModel):
    blank_id: str
    answer: str

# Request
class AnswerBlankRequest(BaseModel):
    flow_session_id: int
    page_num: int
    blank_id: str
    answer: str
    