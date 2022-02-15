from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_blank(db:AsyncSession):
    rows = [
            flowpage_model.Blank(
                id = "blank1",
                flowpage_id = 2,
            ),
            flowpage_model.Blank(
                id = "blank1",
                flowpage_id = 3,
            ),
            flowpage_model.Blank(
                id = "blank2",
                flowpage_id = 3,
            ),
            flowpage_model.Blank(
                id = "blank1",
                flowpage_id = 4,
            ),
            flowpage_model.Blank(
                id = "blank1",
                flowpage_id = 5,
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        