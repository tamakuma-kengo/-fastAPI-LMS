from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_session as flow_session_model

def add_flow_session(db:AsyncSession):
    rows = [
            
    ]
    for row in rows:
        db.add(row)
    db.flush()
        