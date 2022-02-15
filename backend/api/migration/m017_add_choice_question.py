from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_choice_question(db:AsyncSession):
    rows = [
            flowpage_model.ChoiceQuestion(
                id = 5,
                content_id = 8,
                title = "choice_question",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "choice_question",
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        