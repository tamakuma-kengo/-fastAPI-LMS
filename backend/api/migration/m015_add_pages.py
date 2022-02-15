from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_page(db:AsyncSession):
    rows = [
            flowpage_model.Page(
                id = 1,
            ),
    ]
    for row in rows:
        db.add(row)
        