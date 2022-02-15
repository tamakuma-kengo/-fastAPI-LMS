from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
from datetime import datetime

def add_user_kind(db:AsyncSession):
    rows = [
            user_model.UserKind(
                id = 1,
                kind_name = "teacher",
                create = True
            ),
            user_model.UserKind(
                id = 2,
                kind_name = "studnet",
                create = False
            ),
        ]
    for row in rows:
        db.add(row)
    return
