from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_descriptive_text_question(db:AsyncSession):
    rows = [
            flowpage_model.DescriptiveTextQuestion(
                id = 4,
                content_id = 7,
                title = "descriptive_text_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "descriptive_text_question",
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        