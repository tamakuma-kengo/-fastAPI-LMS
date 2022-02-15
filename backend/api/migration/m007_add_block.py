from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.block as block_model

def add_block(db:AsyncSession):
    rows = [
            block_model.Block(
                id = 1,
                course_id = 1,
                content_id = 1,
                order = 0
            ),
            block_model.Block(
                id = 2,
                course_id = 1,
                content_id = 14,
                order = 1
            ),
    ]
    for row in rows:
        db.add(row)
    db.flush()
        