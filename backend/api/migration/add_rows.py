from sqlalchemy.ext.asyncio import AsyncSession

from api.migration.m001_add_user_kind import add_user_kind
from api.migration.m002_add_user import add_user
from api.migration.m003_add_content import add_content
from api.migration.m004_add_course import add_course
from api.migration.m005_add_course_grant import add_course_grant
from api.migration.m006_add_taking_course import add_taking_course
from api.migration.m007_add_block import add_block
from api.migration.m008_add_block_rule import add_block_rule
from api.migration.m009_add_flow import add_flow
from api.migration.m010_add_flow_grant import add_flow_grant
from api.migration.m011_add_flow_rules import add_flow_rules
from api.migration.m012_add_pagegroups import add_pagegroup
from api.migration.m013_add_pages import add_page
from api.migration.m014_add_single_text_questions import add_single_text_question
from api.migration.m015_add_multiple_text_question import add_multiple_text_question
from api.migration.m016_add_descriptive_text_question import add_descriptive_text_question
from api.migration.m017_add_choice_question import add_choice_question
from api.migration.m018_add_choice_question_choice import add_choice_question_choice
from api.migration.m019_add_pagegroup_flow_pages import add_pagegroup_flowpages
from api.migration.m020_add_blank import add_blank
from api.migration.m021_add_correct_answers import add_correct_answer
from api.migration.m022_add_flow_sessions import add_flow_session
from api.migration.m023_add_flow_session_flow_pages import add_flowsession_flowpages
from api.migration.m024_add_flow_session_blank_answer import add_flowsession_blank_answer

def add_rows(db: AsyncSession):
    add_user_kind(db)
    add_user(db)
    add_content(db)
    add_course(db)
    add_course_grant(db)
    add_taking_course(db)
    add_block(db)
    add_block_rule(db)
    add_flow(db)
    add_flow_grant(db)
    add_flow_rules(db)
    add_pagegroup(db)
    add_page(db)
    add_single_text_question(db)
    add_multiple_text_question(db)
    add_descriptive_text_question(db)
    add_choice_question(db)
    add_choice_question_choice(db)
    add_pagegroup_flowpages(db)
    add_blank(db)
    add_correct_answer(db)
    add_flow_session(db)
    add_flowsession_flowpages(db)
    add_flowsession_blank_answer(db)
    
    db.commit()
