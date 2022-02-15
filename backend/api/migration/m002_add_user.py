from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
from datetime import datetime
from api.cruds.domains.generate_hash import get_password_hash

def add_user(db:AsyncSession):
    teachers = [
            user_model.User(
                id = 1, 
                username = "ohno",
                email = "ohno@ohno.com",
                hashed_password = get_password_hash("ohnoohno"),
                user_kind_id = 1,
                is_active = True,
                created = datetime.now()
            ),
            user_model.User(
                id = 2, 
                username = "yanagi",
                email = "yanagi@yanagi.com",
                hashed_password = get_password_hash("yanagiyanagi"),
                user_kind_id = 1,
                is_active = True,
                created = datetime.now()
            ),
            user_model.User(
                id = 3, 
                username = "ogasawara",
                email = "ogasawara@ogasawara.com",
                hashed_password = get_password_hash("ogasawaraogasawara"),
                user_kind_id = 1,
                is_active = True,
                created = datetime.now()
            )
        ]
    for teacher in teachers:
        db.add(teacher)

    students = [
        user_model.User(
            id = 4, 
            username = "okabayashi",
            email = "okabayashi@okabayashi.com",
            hashed_password = get_password_hash("okabayashiokabayashi"),
            user_kind_id = 2,
            is_active = True,
            created = datetime.now()
        ),
        user_model.User(
            id = 5,
            username = "neo",
            email = "neo@neo.com",
            hashed_password = get_password_hash("neoneo"),
            user_kind_id = 2,
            is_active = True,
            created = datetime.now()
        ),
        user_model.User(
            id = 6,
            username = "ishikawa",
            email = "ishikawa@ishikawa.com",
            hashed_password = get_password_hash("ishikawaishikawa"),
            user_kind_id = 2,
            is_active = True,
            created = datetime.now()
        )
    ]
    for student in students:
        db.add(student)
    db.flush()
