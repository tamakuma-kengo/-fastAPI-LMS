from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_single_text_question(db:AsyncSession):
    rows = [
            flowpage_model.SingleTextQuestion(
                id = 2,
                content_id = 5,
                title = "single_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "single_text_question",
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        