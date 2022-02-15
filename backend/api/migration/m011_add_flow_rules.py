from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow as flow_model

def add_flow_rules(db:AsyncSession):
    rows = [
            flow_model.FlowRule(
                flow_id = 1,
                check_answer_timing = "submit_page",
                challenge_limit = None,
                restart_session = True,
                time_limit = None,
                start_date_time = datetime.datetime(2022,2,10,0,0,0),
                end_answer_date_time = datetime.datetime(2023,2,10,0,0,0),
                end_read_date_time = datetime.datetime(2023,2,10,0,0,0),
                always = True
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        