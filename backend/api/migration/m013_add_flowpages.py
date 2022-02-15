from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_flowpages(db:AsyncSession):
    rows = [
            flowpage_model.FlowPage(
                id = 1,
                content_id = 4,
                title = "simple_page",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "page",
            ),
            flowpage_model.FlowPage(
                id = 2,
                content_id = 5,
                title = "single_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "single_text_question",
            ),
            flowpage_model.FlowPage(
                id = 3,
                content_id = 6,
                title = "multiple_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "multiple_text_question",
            ),
            flowpage_model.FlowPage(
                id = 4,
                content_id = 7,
                title = "descriptive_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "descriptive_text_question",
            ),
            flowpage_model.FlowPage(
                id = 5,
                content_id = 8,
                title = "choice_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "choice_question",
            ),
    ]
    for row in rows:
        db.add(row)
        