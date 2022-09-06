from sqlalchemy import Column, Integer, TEXT

from api.db import Base

# コンテンツ情報
class URLLinks(Base):
    __tablename__ = "url_links"

    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, nullable=False, comment="学習する週の番号を格納．")
    study_name = Column(TEXT, nullable=False, comment="学習内容の名前を格納.")
    urls = Column(TEXT, nullable=False, comment="学習内容に関連する外部URLを格納.")
