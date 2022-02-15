from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.page_group as pagegroup_model

def add_pagegroup(db:AsyncSession):
    rows = [
            pagegroup_model.PageGroup(
                id = 1,
                flow_id = 1,
                order = 1,
                shuffle = True,
                num_of_show = None,
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        