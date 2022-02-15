from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_question(db:AsyncSession):
    rows = [
            flowpage_model.Question(
                id = 2,
            ),
            flowpage_model.Question(
                id = 3,
            ),
            flowpage_model.Question(
                id = 4,
            ),
            flowpage_model.Question(
                id = 5,
            ),
    ]
    for row in rows:
        db.add(row)
        