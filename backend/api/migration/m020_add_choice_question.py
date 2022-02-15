from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_choice_question(db:AsyncSession):
    rows = [
            flowpage_model.ChoiceQuestion(
                id = 5,
            ),
    ]
    for row in rows:
        db.add(row)
        