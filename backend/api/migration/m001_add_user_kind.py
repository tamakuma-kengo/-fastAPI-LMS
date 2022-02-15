from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model

def add_user_kind(db:AsyncSession):
    rows = [
            user_model.Userkind(
                id = 1,
                kind_name = "teacher",
                create = True
            ),
             user_model.Userkind(
                id = 2,
                kind_name = "student",
                create = False
            )
        ]
    for row in rows:
        db.add(row)
