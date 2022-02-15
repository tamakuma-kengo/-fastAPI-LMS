from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.block as block_model

def add_block_rule(db:AsyncSession):
    rows = [
            block_model.BlockRule(
                block_id = 1,
                start_date_time = None,
                end_date_time = None,
                always = True
            ),
            block_model.BlockRule(
                block_id = 2,
                start_date_time = None,
                end_date_time = None,
                always = True
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        