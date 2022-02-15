from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.course as course_model

def add_course_grant(db:AsyncSession):
    rows = [
            course_model.CourseGrant(
                user_id = 2,
                course_id = 1,
                start_date_time = datetime.datetime(2022,2,10,0,0,0),
                end_date_time = datetime.datetime(2023,2,10,0,0,0),
                read_answer = True,
                update_answer = True,
                delete_answer = True
            )
    ]
    for row in rows:
        db.add(row)
    db.flush()
        