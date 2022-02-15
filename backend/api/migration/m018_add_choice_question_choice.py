from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_choice_question_choice(db:AsyncSession):
    rows = [
            flowpage_model.ChoiceQuestionChoice(
                id = "choice_1",
                flowpage_id = 5,
                order = 1,
                content_id = 9
            ),
            flowpage_model.ChoiceQuestionChoice(
                id = "choice_2",
                flowpage_id = 5,
                order = 2,
                content_id = 10
            ),
            flowpage_model.ChoiceQuestionChoice(
                id = "choice_3",
                flowpage_id = 5,
                order = 3,
                content_id = 11
            ),
            flowpage_model.ChoiceQuestionChoice(
                id = "choice_4",
                flowpage_id = 5,
                order = 4,
                content_id = 12
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        