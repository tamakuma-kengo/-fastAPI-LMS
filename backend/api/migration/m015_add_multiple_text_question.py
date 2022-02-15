from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_multiple_text_question(db:AsyncSession):
    rows = [
            flowpage_model.MultipleTextQuestion(
                id = 3,
                content_id = 6,
                title = "multiple_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "multiple_text_question",
                answer_column_content_id = 13
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        