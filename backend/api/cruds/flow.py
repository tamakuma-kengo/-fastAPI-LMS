from fastapi import  Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update, func
from typing import List, Optional, Tuple

from api.schemas.user import User
import api.models.content as content_model
import api.models.flow as flow_model
import api.models.flow_session as flow_session_model
import api.models.flow_page as flow_page_model
import api.models.page_group as page_group_model

import api.schemas.course as course_schema
import api.schemas.flow as flow_schema
import api.schemas.flowpage as flowpage_schema

import datetime
import random

async def select_flow(db: AsyncSession,flow_id: int) -> flow_schema.FlowResponse:
    result: Result = await(
        db.execute(
            select(
                flow_model.Flow.title,
                flow_model.FlowRule.check_answer_timing,
                flow_model.FlowRule.challenge_limit,
                flow_model.FlowRule.restart_session,
                flow_model.FlowRule.time_limit,
                flow_model.FlowRule.start_date_time,
                flow_model.FlowRule.end_answer_date_time,
                flow_model.FlowRule.end_read_date_time,
                flow_model.FlowRule.always
            ).where(flow_model.Flow.id == flow_id)
            .where(flow_model.Flow.id == flow_model.FlowRule.flow_id)
        )
    )
    return result.first()

async def select_ids_by_flow_session_id(db: AsyncSession, flow_session_id: int) -> flow_schema.FlowIdResponse:
    result: Result = await(
        db.execute(
            select(
                flow_session_model.FlowSession.flow_id,
                flow_model.Flow.course_id
            ).where(flow_session_model.FlowSession.id == flow_session_id)
            .where(flow_model.Flow.id == flow_session_model.FlowSession.flow_id)
        )
    )
    return result.first()
    
async def select_flow_info(db: AsyncSession,flow_session_id: int) -> flow_schema.FlowInfoResponse:
    result: Result = await(
        db.execute(
            select(
                flow_model.Flow.title.label("flow_title"),
                func.count("*").label("num_of_pages")
            ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
            .where(flow_model.Flow.id == flow_session_model.FlowSession.flow_id)
            .where(flow_session_model.FlowSession.id == flow_session_model.FlowSessionFlowPage.flow_session_id)
        )
    )
    return result.first()

async def select_flow_welcome_page(db: AsyncSession,flow_id: int) -> flow_schema.ContentResponse:
    result: Result = await(
        db.execute(
            select(
                content_model.Content.content
            ).where(flow_model.Flow.id == flow_id)
            .where(flow_model.Flow.welcome_page_content_id == content_model.Content.id)
        )
    )
    return result.first()

async def select_flow_completion_page(db: AsyncSession,flow_id: int) -> flow_schema.ContentResponse:
    result: Result = await(
        db.execute(
            select(
                content_model.Content.content
            ).where(flow_model.Flow.id == flow_id)
            .where(flow_model.Flow.completion_page_content_id == content_model.Content.id)
        )
    )
    return result.first()

async def select_flow_sessions(db: AsyncSession,flow_id: int, user_id: int) -> List[flow_schema.FlowSessionResponse]:
    result: Result = await(
        db.execute(
            select(
                flow_session_model.FlowSession.id,
                flow_session_model.FlowSession.start_date_time,
                flow_session_model.FlowSession.finish_date_time,
                flow_session_model.FlowSession.is_finished
            ).where(flow_session_model.FlowSession.user_id == user_id)
            .where(flow_session_model.FlowSession.flow_id == flow_id)
        )
    )
    return result.all()

async def insert_flow_session(db: AsyncSession, flow_id: int, user_id: int) -> flow_schema.StartFlowSessionResonse:
    new_flow_session = flow_schema.FlowSessionCreate(user_id=user_id, flow_id=flow_id, start_date_time=datetime.datetime.now())
    row = flow_session_model.FlowSession(**new_flow_session.dict())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    response = {"start_success": True, "flow_session_id": row.id, "start_date_time": row.start_date_time}
    return flow_schema.StartFlowSessionResonse(**response)

async def select_page_groups(db: AsyncSession, flow_id: int) -> List[page_group_model.PageGroup]:
    result: Result = await(
        db.execute(
            select(
                page_group_model.PageGroup.id,
                page_group_model.PageGroup.flow_id,
                page_group_model.PageGroup.order,
                page_group_model.PageGroup.shuffle,
                page_group_model.PageGroup.num_of_show
            ).where(page_group_model.PageGroup.flow_id == flow_id)
            .order_by(page_group_model.PageGroup.order)
        )
    )
    return result.all()

async def select_pagegroup_flowpages(db: AsyncSession, page_group_id: int) -> List[page_group_model.PageGroupFlowPages]:
    result: Result = await(
        db.execute(
            select(
                page_group_model.PageGroupFlowPages.pagegroup_id,
                page_group_model.PageGroupFlowPages.flowpage_id,
                page_group_model.PageGroupFlowPages.order
            ).where(page_group_model.PageGroupFlowPages.pagegroup_id == page_group_id)
            .order_by(page_group_model.PageGroupFlowPages.order)
        )
    )
    return result.all()

async def insert_flow_session_flow_page(db: AsyncSession, flow_session_flow_pages: List[flow_session_model.FlowSessionFlowPage]):
    db.add_all(flow_session_flow_pages)
    await db.commit()
    return

async def select_flow_session_by_id(db: AsyncSession, flow_session_id: int) -> flow_session_model.FlowSession:
    result: Result = await(
        db.execute(
            select(
                flow_session_model.FlowSession.id,
                flow_session_model.FlowSession.user_id,
                flow_session_model.FlowSession.flow_id,
                flow_session_model.FlowSession.start_date_time,
                flow_session_model.FlowSession.finish_date_time,
                flow_session_model.FlowSession.is_finished
            ).where(flow_session_model.FlowSession.id == flow_session_id)
        )
    )
    return flow_session_model.FlowSession(**result.first())

async def update_to_finish_flow_session(db: AsyncSession, flow_session_id: int):
    finish_date_time = datetime.datetime.now()
    result: Result = await(
        db.execute(
            update(flow_session_model.FlowSession)
            .where(flow_session_model.FlowSession.id==flow_session_id)
            .values(is_finished=True,finish_date_time=finish_date_time)
        )
    )
    await db.commit()
    return {"finish_success": True, "finish_date_time": finish_date_time}

async def select_simple_page(db: AsyncSession, flowpage_id: int) -> flowpage_schema.PageResponse:
    result: Result = await(
        db.execute(
            select(
                content_model.Content.content,
            ).where(flow_page_model.Page.id == flowpage_id)
            .where(flow_page_model.Page.content_id == content_model.Content.id)
        )
    )
    return result.first()

async def select_single_text_question(db: AsyncSession, flowpage_id: int) -> flowpage_schema.SingleTextQuestionResponse:
    result: Result = await(
        db.execute(
            select(
                flow_page_model.SingleTextQuestion.id,
                content_model.Content.content,
                flow_page_model.Blank.id.label("blank_id")
            ).where(flow_page_model.SingleTextQuestion.id == flowpage_id)
            .where(flow_page_model.SingleTextQuestion.content_id == content_model.Content.id)
            .where(flow_page_model.SingleTextQuestion.id == flow_page_model.Blank.flowpage_id)
        )
    )
    return result.first()

async def select_multiple_text_question(db: AsyncSession, flowpage_id: int) -> flowpage_schema.MultipleTextQuestionResponse:
    print(flowpage_id)
    content_result: Result = await(
        db.execute(
            select(
                flow_page_model.FlowPage.id, 
                content_model.Content.content.label("content"),
            ).where(flow_page_model.FlowPage.id == flowpage_id)
            .where(flow_page_model.FlowPage.content_id == content_model.Content.id)
        )
    )
    answer_column_result: Result = await(
        db.execute(
            select(
                    flow_page_model.MultipleTextQuestion.id, 
                    content_model.Content.content.label("answer_column_content"),
            ).where(flow_page_model.MultipleTextQuestion.id == flowpage_id)
            .where(flow_page_model.MultipleTextQuestion.answer_column_content_id == content_model.Content.id)
        )
    )
    content = content_result.mappings().first()["content"]
    answer_column = answer_column_result.mappings().first()["answer_column_content"]
    return  {"content": content, "answer_column_content": answer_column}

async def select_descriptive_text_question(db: AsyncSession, flowpage_id: int) -> flowpage_schema.DescriptiveTextQuestionResponse:
    result: Result = await(
        db.execute(
            select(
                content_model.Content.content,
                flow_page_model.Blank.id.label("blank_id")
            ).where(flow_page_model.DescriptiveTextQuestion.id == flowpage_id)
            .where(flow_page_model.DescriptiveTextQuestion.id == flow_page_model.FlowPage.id)
            .where(flow_page_model.DescriptiveTextQuestion.content_id == content_model.Content.id)
            .where(flow_page_model.DescriptiveTextQuestion.id == flow_page_model.Blank.flowpage_id)
        )
    )
    return result.first()

async def select_choice_question_choices(db: AsyncSession, flowpage_id: int) -> List[flowpage_schema.ChoiceQuestionChoiceResponse]:
    result: Result = await(
        db.execute(
            select(
                flow_page_model.ChoiceQuestionChoice.id,
                content_model.Content.content,
                flow_page_model.ChoiceQuestionChoice.order
            ).where(flow_page_model.ChoiceQuestionChoice.flowpage_id == flowpage_id)
            .where(flow_page_model.ChoiceQuestionChoice.content_id == content_model.Content.id)
        )
    )
    return result.all()

async def select_choice_question(db: AsyncSession, flowpage_id: int) -> flowpage_schema.ChoiceQuestionResponse:
    choice_question_result: Result = await(
        db.execute(
            select(
                content_model.Content.content,
                flow_page_model.Blank.id.label("blank_id")
            ).where(flow_page_model.ChoiceQuestion.id == flowpage_id)
            .where(flow_page_model.ChoiceQuestion.content_id == content_model.Content.id)
            .where(flow_page_model.ChoiceQuestion.id == flow_page_model.Blank.flowpage_id)
        )
    )

    choice_result_dict = choice_question_result.mappings().first()
    choices_result = await select_choice_question_choices(db=db, flowpage_id=flowpage_id)

    response = {
        "content": choice_result_dict["content"],
        "blank_id": choice_result_dict["blank_id"],
        "choices": choices_result
        }
    return response

async def select_flow_session_flowpage(db: AsyncSession, flow_session_id: int, page_num: int):
    flow_page_result: Result = await(
        db.execute(
            select(
                flow_page_model.FlowPage.id,
                flow_page_model.FlowPage.title,
                flow_page_model.FlowPage.page_type
            ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
            .where(flow_session_model.FlowSessionFlowPage.order == page_num)
            .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flow_page_model.FlowPage.id)
            .where(flow_page_model.FlowPage.content_id == content_model.Content.id)
        )
    )
    flow_page_dict = flow_page_result.mappings().first()
    page_type = flow_page_dict["page_type"]

    print(flow_page_dict)

    if page_type in ["page","Page"]:
        page_type = "SimplePage"
        page_content = await select_simple_page(db=db, flowpage_id = flow_page_dict["id"])
    elif page_type in ["single_text_question","SingleTextQuestion"]:
        page_type = "SingleTextQuestion"
        page_content = await select_single_text_question(db=db, flowpage_id = flow_page_dict["id"])
    elif page_type in ["multiple_text_question","MultipleTextQuestion"]:
        page_type = "MultipleTextQuestion"
        page_content = await select_multiple_text_question(db=db, flowpage_id = flow_page_dict["id"])
    elif page_type in ["descriptive_text_question","DescriptiveTextQuestion"]:
        page_type = "DescriptiveTextQuestion"
        page_content = await select_descriptive_text_question(db=db, flowpage_id = flow_page_dict["id"])
    elif page_type in ["choice_question","ChoiceQuestion"]:
        page_type = "ChoiceQuestion"
        page_content = await select_choice_question(db=db, flowpage_id = flow_page_dict["id"])
    else:
        raise ValueError(f"page_type: {page_type} is not defined.")

    response = {
        "title": flow_page_dict["title"],
        "page_type": page_type,
        "page_content": page_content
    }
    return response

async def select_flow_session_flowpage_answer(db: AsyncSession, flow_session_id: int, page_num: int) -> flowpage_schema.BlankAnswerResponse:
    result: Result = await(
        db.execute(
            f"""
            select tb_a.blank_id, tb_a.answer
            from 
            (
                select flow_session_flow_pages.flowpage_id,  flow_session_blank_answer.blank_id, flow_session_blank_answer.answer, flow_session_blank_answer.created
                from flow_session_blank_answer 
                inner join 
                flow_session_flow_pages
                on flow_session_blank_answer.flow_session_id = flow_session_flow_pages.flow_session_id
                and flow_session_blank_answer.flowpage_id = flow_session_flow_pages.flowpage_id
                where flow_session_flow_pages.flow_session_id = {flow_session_id}
                and flow_session_flow_pages.order = {page_num}
            ) tb_a
            inner join
            (
                select flow_session_flow_pages.flowpage_id, flow_session_blank_answer.blank_id, max(flow_session_blank_answer.created) as latest_created
                from flow_session_blank_answer 
                inner join 
                flow_session_flow_pages
                on flow_session_blank_answer.flow_session_id = flow_session_flow_pages.flow_session_id
                and flow_session_blank_answer.flowpage_id = flow_session_flow_pages.flowpage_id
                where flow_session_flow_pages.flow_session_id = {flow_session_id}
                and flow_session_flow_pages.order = {page_num}
                group by  flow_session_flow_pages.flowpage_id, flow_session_blank_answer.blank_id
            ) tb_b
            on tb_a.flowpage_id = tb_b.flowpage_id
            and tb_a.blank_id = tb_b.blank_id
            and tb_a.created = tb_b.latest_created 
            """
        )
    )
    return result.all()

async def insert_blank_answer(db: AsyncSession, answer_blank_request:List[flowpage_schema.AnswerBlankRequest]):
    for answer_blank in answer_blank_request:
        result: Result = await(
            db.execute(
                select(
                    flow_session_model.FlowSessionFlowPage.flowpage_id,
                ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == answer_blank.flow_session_id)
                .where(flow_session_model.FlowSessionFlowPage.order == answer_blank.page_num)
            )
        )
        flowpage_id = result.mappings().first()["flowpage_id"]

        new_flow_session_blank_answer = flow_schema.FlowSessionBlankAnswerCreate(
            flow_session_id = answer_blank.flow_session_id,
            flowpage_id = flowpage_id,
            blank_id = answer_blank.blank_id,
            answer = answer_blank.answer,
            created = datetime.datetime.now()
        )
        row = flow_session_model.FlowSessionBlankAnswer(**new_flow_session_blank_answer.dict())
        db.add(row)
    await db.commit()
    return 

async def is_readable_flow(db: AsyncSession, flow_id: int, user: User):
    return True

async def get_flow(db: AsyncSession, flow_id: int):
    return await select_flow(db=db, flow_id=flow_id)

async def get_ids_by_flow_session_id(db: AsyncSession, flow_session_id: int):
    return await select_ids_by_flow_session_id(db=db, flow_session_id=flow_session_id)

async def get_flow_info(db: AsyncSession, flow_session_id: int):
    return await select_flow_info(db=db, flow_session_id=flow_session_id)

async def get_flow_welcome_page(db: AsyncSession, flow_id: int):
    return await select_flow_welcome_page(db=db, flow_id=flow_id)

async def get_flow_completion_page(db: AsyncSession, flow_id: int):
    return await select_flow_completion_page(db=db, flow_id=flow_id)

async def get_flow_sessions(db: AsyncSession, flow_id: int, user_id: int):
    return await select_flow_sessions(db=db, flow_id=flow_id, user_id=user_id)

async def is_startable_flow_session(db: AsyncSession, flow_id: int, user_id: int):
    return True

async def start_new_flow_session(db: AsyncSession, flow_id: int, user_id: int):
    start_flow_session_response = await insert_flow_session(db=db, flow_id=flow_id, user_id=user_id)
    flow_groups = await select_page_groups(db=db, flow_id=flow_id)
    order_in_flow_session = 1
    flow_session_flow_page_list = []
    for flow_group in flow_groups:
        pagegroup_flowpages = await select_pagegroup_flowpages(db=db, page_group_id=flow_group.id)
        if flow_group.shuffle:
            random.seed(datetime.datetime.now().microsecond)
            random.shuffle(pagegroup_flowpages)
        
        num_of_show = len(pagegroup_flowpages) if flow_group.num_of_show == None else flow_group.num_of_show
        for pagegroup_flowpage in pagegroup_flowpages[:num_of_show]:
            flow_session_flow_page_list += [
                flow_session_model.FlowSessionFlowPage(
                    flow_session_id = start_flow_session_response.flow_session_id,
                    flowpage_id = pagegroup_flowpage.flowpage_id,
                    order = order_in_flow_session,
                    submitted = False
                )
            ]
            order_in_flow_session += 1
    await insert_flow_session_flow_page(db=db, flow_session_flow_pages=flow_session_flow_page_list)
    return start_flow_session_response

async def finish_flow_session(db: AsyncSession, flow_session_id: int):
    # original_flow_session = await select_flow_session_by_id(db=db, flow_session_id=flow_session_id)
    # new = flow_session_model.FlowSession(id=11,user_id=5,flow_id=1,start_date_time=datetime.datetime(2022,2,17,1,25,30),finish_date_time=datetime.datetime(2022,2,17,2,25,30),is_finished=True)
    return await update_to_finish_flow_session(db=db, flow_session_id=flow_session_id)    

async def get_flow_session_flowpage(db: AsyncSession, flow_session_id: int, page_num: int):
    return await select_flow_session_flowpage(db=db, flow_session_id=flow_session_id, page_num=page_num)

async def get_flow_session_flowpage_answer(db: AsyncSession, flow_session_id: int, page_num: int):
    return await select_flow_session_flowpage_answer(db=db, flow_session_id=flow_session_id, page_num=page_num)

async def register_blank_answer(db: AsyncSession, answer_blank_request: List[flowpage_schema.AnswerBlankRequest]):
    return await insert_blank_answer(db=db, answer_blank_request=answer_blank_request)
    