from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_simple_text_question(db:AsyncSession):
    rows = [
            flowpage_model.SingleTextQuestion(
                id = 2,
            ),
    ]
    for row in rows:
        db.add(row)
        