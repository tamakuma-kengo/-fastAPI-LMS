from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow as flow_model

def add_flow(db:AsyncSession):
    rows = [
            flow_model.Flow(
                id = 1,
                id_in_yml = "sample_flow",
                course_id = 1,
                title = "sample_flow",
                created = datetime.datetime(2022,2,10,0,0,0),
                welcome_page_content_id = 2,
                completion_page_content_id = 3 
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        