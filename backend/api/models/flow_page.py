
# ページを示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

from datetime import datetime

from api.db import Base

# ページ情報
class FlowPage(Base):
    __tablename__ = "flowpages"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    title = Column(String(128), nullable=False, comment="ページのタイトル.")
    created = Column(DATETIME,default=datetime.now(), nullable=False)
    page_type = Column(String(128), nullable=False, comment="ページのタイプ")

# 解答機能を持たないページ
class Page(FlowPage):
    __tablename__ = "pages"

    id = Column(Integer, ForeignKey("flowpages.id"), primary_key=True)

    flowpage = relationship("FlowPage")

# 解答機能を持つページ
class Question(FlowPage):
    __tablename__ = "questions"

    id = Column(Integer, ForeignKey("flowpages.id"), primary_key=True)

    blank = relationship("Blank", back_populates="question")
    flowpage = relationship("FlowPage")

# 単一解答の問題を持つページ
class SingleTextQuestion(Question):
    __tablename__ = "single_text_questions"

    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

    question = relationship("Question")

# 複数解答の問題を持つページ
class MultipleTextQuestion(Question):
    __tablename__ = "multiple_text_questions"

    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    answer_column_content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    question = relationship("Question")

# 自由記述の問題を持つページ
class DescriptiveTextQuestion(Question):
    __tablename__ = "descriptive_text_questions"

    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

    question = relationship("Question")

# 解答欄の情報
class ChoiceQuestion(Question):
    __tablename__ = "choice_questions"

    id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

    choice_question_choice = relationship("ChoiceQuestionChoice", back_populates="choice_question")
    question = relationship("Question")

# 選択式の問題の選択肢
class ChoiceQuestionChoice(Base):
    __tablename__ = "choice_question_choices"

    id = Column(String(256), primary_key=True)
    flowpage_id = Column(Integer, ForeignKey("choice_questions.id"), primary_key=True)
    order = Column(Integer, nullable=False, comment="選択肢内での表示順序. 小さいものから順に表示される. 同じページ内で一意.")
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

    choice_question = relationship("ChoiceQuestion", back_populates="choice_question_choice")

# 解答欄の情報
class Blank(Base):
    __tablename__ = "blanks"

    id = Column(String(256), primary_key=True)
    flowpage_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

    question = relationship("Question", back_populates="blank")

# 正答情報
class CorrectAnswer(Base):
    __tablename__ = "correct_answers"

    id = Column(Integer, primary_key=True, index=True)
    flowpage_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    blank_id = Column(String(256), ForeignKey("blanks.id"), nullable=False)
    type = Column(String(32), nullable=False, comment="問題の型. ")
    value = Column(String(256), nullable=False, comment="問題の正答. ")
