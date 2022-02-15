from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_correct_answer(db:AsyncSession):
    rows = [
            flowpage_model.CorrectAnswer(
                id = 1,
                flowpage_id = 2,
                blank_id = "blank1",
                type = "str",
                value = "14"
            ),
            flowpage_model.CorrectAnswer(
                id = 2,
                flowpage_id = 2,
                blank_id = "blank1",
                type = "int",
                value = "14"
            ),
            flowpage_model.CorrectAnswer(
                id = 3,
                flowpage_id = 3,
                blank_id = "blank1",
                type = "int",
                value = "1"
            ),
            flowpage_model.CorrectAnswer(
                id = 4,
                flowpage_id = 3,
                blank_id = "blank2",
                type = "int",
                value = "2"
            ),
            flowpage_model.CorrectAnswer(
                id = 5,
                flowpage_id = 5,
                blank_id = "blank1",
                type = "str",
                value = "choice_1"
            ),
            flowpage_model.CorrectAnswer(
                id = 6,
                flowpage_id = 5,
                blank_id = "blank1",
                type = "str",
                value = "choice_2"
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        