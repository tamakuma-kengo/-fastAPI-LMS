from urllib import response
from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Response
from typing import List,Optional

from api.schemas.token import Token
import api.schemas.flow as flow_schema
import api.schemas.flowpage as flowpage_schema
import api.cruds.flow as flow_crud
from api.schemas.user import User
import api.cruds.user as user_crud

from api.db import get_db
from datetime import timedelta

router = APIRouter()

@router.get("/get_flow/{flow_id}", response_model=flow_schema.FlowResponse)
async def get_flow(flow_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow(db, flow_id)

@router.get("/get_ids_by_flow_session_id/{flow_session_id}", response_model=flow_schema.FlowIdResponse)
async def get_ids_by_flow_session_id(flow_session_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.get_ids_by_flow_session_id(db=db, flow_session_id=flow_session_id)

@router.get("/get_flow_info/{flow_session_id}", response_model=flow_schema.FlowInfoResponse)
async def get_flow(flow_session_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    # is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    # if not is_readalbe:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow_info(db, flow_session_id)

@router.get("/get_flow_welcome_page/{flow_id}", response_model=flow_schema.ContentResponse)
async def get_flow(flow_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow_welcome_page(db, flow_id)

@router.get("/get_flow_completion_page/{flow_id}", response_model=flow_schema.ContentResponse)
async def get_flow(flow_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow_completion_page(db, flow_id)

@router.get("/get_flow_sessions/{flow_id}", response_model=List[flow_schema.FlowSessionResponse])
async def get_flow_sessions(flow_id: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_sessions(db, flow_id, user.id)

@router.post("/start_new_flow_session", response_model=flow_schema.StartFlowSessionResonse)
async def start_new_flow_session(start_flow_session_request: flow_schema.StartFlowSessionRequest, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_startable = await flow_crud.is_startable_flow_session(db, start_flow_session_request.flow_id, user.id)
    if not is_startable:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.start_new_flow_session(db, start_flow_session_request.flow_id, user.id)

@router.post("/finish_flow_session", response_model=flow_schema.FinishFlowSessionResonse)
async def finish_flow_session(finish_flow_session_request: flow_schema.FinishFlowSessionRequest, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.finish_flow_session(db, finish_flow_session_request.flow_session_id)

@router.get("/get_flowpage/{flow_session_id}/{page_num}")
async def get_flowpage(flow_session_id: int, page_num: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_flowpage(db, flow_session_id, page_num)

@router.get("/get_blank_answer/{flow_session_id}/{page_num}", response_model=List[flowpage_schema.BlankAnswerResponse])
async def get_flowpage(flow_session_id: int, page_num: int, user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_flowpage_answer(db, flow_session_id, page_num)

@router.post("/register_blank_answer", response_model=List[flow_schema.RegisterAnswerResponse])
async def register_blank_answer(answer_blank_request: List[flowpage_schema.AnswerBlankRequest], user: User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.register_blank_answer(db, answer_blank_request)
