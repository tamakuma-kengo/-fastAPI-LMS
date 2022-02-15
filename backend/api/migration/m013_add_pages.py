from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flowpage_model

def add_page(db:AsyncSession):
    rows = [
            flowpage_model.Page(
                id = 1,
                content_id = 4,
                title = "simple_page",
                created = datetime.datetime(2022,2,10,0,0,0),
                page_type = "page",
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        