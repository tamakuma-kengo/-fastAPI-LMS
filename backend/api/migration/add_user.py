from tkinter.tix import Tree
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.user import UserCreate, UserKindCreate
import api.models.user as user_model
from datetime import datetime
from api.cruds.domains.generate_hash import get_password_hash

# 教員を追加
def add_teacher(db:AsyncSession):
    user_kind_teacher = UserKindCreate(
            kind_name = "teacher",
            create = True
        )
    row = user_model.UserKind(**user_kind_teacher.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    teacher_kind_id = row.id

    teachers = [
        UserCreate(
            username = "ohno",
            email = "ohno@ohno.com",
            hashed_password = get_password_hash("ohnoohno"),
            user_kind_id = teacher_kind_id,
            is_active = True,
            created = datetime.now()
        ),
        UserCreate(
            username = "yanagi",
            email = "yanagi@yanagi.com",
            hashed_password = get_password_hash("yanagiyanagi"),
            user_kind_id = teacher_kind_id,
            is_active = True,
            created = datetime.now()
        ),
        UserCreate(
            username = "ogasawara",
            email = "ogasawara@ogasawara.com",
            hashed_password = get_password_hash("ogasawaraogasawara"),
            user_kind_id = teacher_kind_id,
            is_active = True,
            created = datetime.now()
        )
    ]
    for teacher in teachers:
        row = user_model.User(**teacher.dict())
        db.add(row)
        db.commit()
        db.refresh(row)


# 生徒を追加
def add_student(db:AsyncSession):
    user_kind_student = UserKindCreate(
            kind_name = "students",
            create = False
        )
    row = user_model.UserKind(**user_kind_student.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    student_kind_id = row.id
    students = [
        UserCreate(
            username = "okabayashi",
            email = "okabayashi@okabayashi.com",
            hashed_password = get_password_hash("okabayashiokabayashi"),
            user_kind_id = student_kind_id,
            is_active = True,
            created = datetime.now()
        ),
        UserCreate(
            username = "neo",
            email = "neo@neo.com",
            hashed_password = get_password_hash("neoneo"),
            user_kind_id = student_kind_id,
            is_active = True,
            created = datetime.now()
        ),
        UserCreate(
            username = "ishikawa",
            email = "ishikawa@ishikawa.com",
            hashed_password = get_password_hash("ishikawaishikawa"),
            user_kind_id = student_kind_id,
            is_active = True,
            created = datetime.now()
        )
    ]
    for student in students:
        row = user_model.User(**student.dict())
        db.add(row)
        db.commit()
        db.refresh(row)

def add_users(db: AsyncSession):
    add_teacher(db)
    add_student(db)
