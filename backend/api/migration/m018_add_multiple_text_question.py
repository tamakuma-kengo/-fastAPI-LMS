from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_multiple_text_question(db:AsyncSession):
    rows = [
            flowpage_model.MultipleTextQuestion(
                id = 3,
                answer_column_content_id = 13
            ),
    ]
    for row in rows:
        db.add(row)
        