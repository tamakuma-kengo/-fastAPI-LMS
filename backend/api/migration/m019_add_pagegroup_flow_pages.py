from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.page_group as pagegroup_model

def add_pagegroup_flowpages(db:AsyncSession):
    rows = [
            pagegroup_model.PageGroupFlowPages(
                pagegroup_id = 1,
                flowpage_id = 1,
                order = 1
            ),
            pagegroup_model.PageGroupFlowPages(
                pagegroup_id = 1,
                flowpage_id = 2,
                order = 2
            ),
            pagegroup_model.PageGroupFlowPages(
                pagegroup_id = 1,
                flowpage_id = 3,
                order = 3
            ),
            pagegroup_model.PageGroupFlowPages(
                pagegroup_id = 1,
                flowpage_id = 4,
                order = 4
            ),
            pagegroup_model.PageGroupFlowPages(
                pagegroup_id = 1,
                flowpage_id = 5,
                order = 5
            )
    ]
    for row in rows:
        db.add(row)
    db.flush()
        