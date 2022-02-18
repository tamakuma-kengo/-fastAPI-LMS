from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.content as content_model

def add_content(db:AsyncSession):
    rows = [
            content_model.Content(
                id = 1,
                content = "これはコースのトップページです.\nフローへのリンク[フロー](1/flow/1)",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 2,
                content = "これはフローの最初に表示されるページです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 3,
                content = "これはフローの最後に表示されるページです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 4,
                content = "シンプルなページです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 5,
                content = "SingleTextQuestionです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 6,
                content = "MultipleTextQuestionです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 7,
                content = "DescriptiveTextQuestionです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 8,
                content = "ChoiceQuestionです\naから始める単語を選択してください.",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 9,
                content = "Apple",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 10,
                content = "Ant",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 11,
                content = "Orange",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 12,
                content = "Banana",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 13,
                content = "回答欄1:[[blank1]] 回答欄2:[[blank2]]",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
            content_model.Content(
                id = 14,
                content = "これはコースページの2つ目のブロックです",
                created = datetime.datetime(2022,2,10,0,0,0)
            ),
        ]
    for row in rows:
        db.add(row)
    db.flush()
