from audioop import add
from fastapi import  Depends,HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert
from typing import List, Optional, Tuple
import datetime


from api.schemas.user import HomeUserProfile, User, UserCreate, UserWithGrant
import api.models.course as course_model
import api.models.content as content_model
import api.models.block as block_model

import api.schemas.content as content_schema
import api.schemas.block as block_schema
from api.cruds.user import get_home_profile
import api.schemas.course as course_schema
from api.db import get_db

import yamale
import yaml
import traceback
import re

class YamlFormatter():
    def __init__(self,files:List[course_schema.RegisterCourseRequest]):
        self.directory_structure = self.create_directry_structure(files)
        self.course_yml_dict = {}
        self.flow_yml_list = []

    def create_directry_structure(self,files:List[course_schema.RegisterCourseRequest]):
        directory_structure = {}
        for file in files:
            new_dict = directory_structure
            splited_path = file.file_path.split("/")
            file_name = splited_path[-1]
            for dir in splited_path[:-1]:
                if dir in new_dict:
                    new_dict = new_dict[dir]
                else:
                    new_dict[dir] = {}
                    new_dict = new_dict[dir]
            new_dict[file_name] = file.file_text
        return directory_structure

    def get_file_by_path(self,path):
        path_splited = path.split("/")
        file_name = path_splited[-1]
        d = self.directory_structure[self.root_directory]
        for dir in path_splited[:-1]:
            d = d[dir]
        return d[file_name]

    def replace_scripts(self,yml_text:str):
        scripts = re.findall('(\s*?){{\s*(.+?)\s*\((.+?)\)\s*}}',yml_text)
        for script in scripts:
            num_indent_spaces = len(script[0])
            if script[1] == "include":
                included_yml = self.get_file_by_path(script[2])
                included_yml = self.replace_scripts(included_yml)
                included_yml_with_indent = "\n"
                for line in included_yml.split("\n"):
                    new_line = " "*num_indent_spaces+line+"\n"
                    included_yml_with_indent += new_line
                yml_text = re.sub(f'{script[0]}{{{{{script[1]}\s*\({script[2]}\)}}}}',included_yml_with_indent,yml_text)
        return yml_text

    def validate_course(self,yml_text:str):
        validate_error = []
        try:
            schema = yamale.make_schema('./api/yaml_validation_schemas/course.yml')
            self.course_yml_dict = yaml.safe_load(yml_text)
            data = [(self.course_yml_dict,'')]
            yamale.validate(schema,data)
            # flowリンクの存在チェック
            flow_links = re.findall('\(\s*flow\s*:\s*(.+?)\s*\)',yml_text,re.S)
            for link in flow_links:
                if not link[0] in self.directory_structure[self.root_directory]["flows"]:
                    validate_error += [f"flow_file '{link[0]}' is not found."]
        except ValueError as e:
            t = traceback.format_exception_only(type(e),e)
            validate_error += t
        return {"success":len(validate_error)==0,"error_msgs":validate_error}

    def validate_flow(self,yml_text:str):
        validate_error = []
        try:
            # Flowファイルのバリデーション
            yml_text = self.replace_scripts(yml_text= yml_text)
            schema = yamale.make_schema('./api/yaml_validation_schemas/flow.yml')
            flow_yml_dict = yaml.safe_load(yml_text)
            self.flow_yml_list += [flow_yml_dict]
            flow_data = [(flow_yml_dict,'')]
            yamale.validate(schema,flow_data)

            ## ページタイプ別のバリデーション
            for page_group in flow_yml_dict["page_groups"]:
                for page in page_group["pages"]:
                    page_data = [(page,'')]
                    try:
                        page_type = page["page_type"]
                        # シンプルページのバリデーション
                        if page_type in ["page","Page"]:
                            schema = yamale.make_schema('./api/yaml_validation_schemas/pages/page.yml')
                            yamale.validate(schema,page_data)
                        # SingleTextQuestionのバリデーション
                        elif page_type in ["SingleTextQuestion","single_text_question"]:
                            schema = yamale.make_schema('./api/yaml_validation_schemas/pages/single_text_question.yml')
                            yamale.validate(schema,page_data)
                        # MultipleTextQuestionのバリデーション
                        elif page_type in ["MultipleTextQuestion","multiple_text_question"]:
                            schema = yamale.make_schema('./api/yaml_validation_schemas/pages/multiple_text_question.yml')
                            yamale.validate(schema,page_data)
                            # blank_idのチェック
                            answer_column_blank_id = re.findall('\[\[(.+?)\]\]',page["answer_column"])
                            correct_answer_blank_id = [ v["blank_id"] for v in page["correct_answers"]]
                            if len(answer_column_blank_id) != len(set(answer_column_blank_id)):
                                raise ValueError("There is blank_id duplicate in answer_column.")
                            if len(correct_answer_blank_id) != len(set(correct_answer_blank_id)):
                                raise ValueError("There is blank_id duplicate in correct_answers.")
                            if not set(answer_column_blank_id) == set(correct_answer_blank_id):
                                raise ValueError("There is no ID correspondence between answer_column and correct_answers.")
                        # DescriptiveTextQuestionのバリデーション
                        elif page_type in ["DescriptiveTextQuestion","descriptive_text_question"]:
                            schema = yamale.make_schema('./api/yaml_validation_schemas/pages/descriptive_text_question.yml')
                            yamale.validate(schema,page_data)
                        # ChoiceQuestionのバリデーション
                        elif page_type in ["ChoiceQuestion","choice_question"]:
                            schema = yamale.make_schema('./api/yaml_validation_schemas/pages/choice_question.yml')
                            yamale.validate(schema,page_data)
                            # choice_idのチェック
                            choices_id = [v["choice_id"] for v in page["choices"]]
                            corecct_choice_id = page["correct_choices"]
                            if len(choices_id) != len(set(choices_id)):
                                raise ValueError("There is blank_id duplicate in choices.")
                            if len(corecct_choice_id) != len(set(corecct_choice_id)):
                                raise ValueError("There is blank_id duplicate in correct_choices.")
                            print(choices_id,corecct_choice_id)
                            if not set(choices_id) >= set(corecct_choice_id):
                                raise ValueError("There is no ID correspondence between choices and correct_choices.")
                        else:
                            raise ValueError(f"page_type: {page_type} is not defined.")
                    except ValueError as e:
                        t = traceback.format_exception_only(type(e),e)
                        validate_error += t
        except ValueError as e:
            t = traceback.format_exception_only(type(e),e)
            validate_error += t
        return {"success":len(validate_error)==0,"error_msgs":validate_error}

    def validate_files(self):
        error_msg = ""

        ## course.ymlのバリデーション
        course_validation_success = False
        if len(self.directory_structure.keys()) != 1:
            error_msg += "ルートディレクトリは1つ"
            return {"sccess":False,"error_msg":error_msg}
        self.root_directory = list(self.directory_structure.keys())[0]
        if "course.yml" not in self.directory_structure[self.root_directory] and  "course.yaml" not in self.directory_structure[self.root_directory]:
            error_msg += "course.ymlが見つかりません."
        elif "course.yml" in self.directory_structure and "course.yaml" in self.directory_structure:
            error_msg += "course.ymlが複数見つかりました."
        else:
            course_yml = self.directory_structure[self.root_directory]["course.yml"] if "course.yml" in self.directory_structure[self.root_directory] \
                else self.directory_structure[self.root_directory]["course.yaml"]
            course_validate = self.validate_course(course_yml)
            course_validation_success = course_validate["success"]
            if not course_validate["success"]:
                error_msg += "\n".join(course_validate["error_msgs"])

        ## flowのバリデーション
        course_validation_success = True
        if "flows" in self.directory_structure[self.root_directory]:
            flow_files = self.directory_structure[self.root_directory]["flows"].keys()
            for flow_file in flow_files:
                if not re.match('.*\.(yaml|yml)$',flow_file):
                    error_msg += f"{flow_file} is not yml_file\n"
                flow_validate = self.validate_flow(self.directory_structure[self.root_directory]["flows"][flow_file])
                course_validation_success = course_validation_success and flow_validate["success"]
                if not course_validation_success:
                    error_msg += "\n".join(flow_validate["error_msgs"])
        
        ## 書き込み可否
        if course_validation_success and  course_validation_success:
            return {"success":True, "error_msg":error_msg}
        return {"success":False, "error_msg":error_msg}

async def add_course(db: AsyncSession, register_course_request:course_schema.RegisterCourseRequest):
    new_course = course_schema.CourseCreate(course_name=register_course_request.course_name,start_date_time=register_course_request.start_date_time,end_date_time=register_course_request.end_date_time)
    row = course_model.Course(**new_course.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return course_schema.RegisteredCourse(id=row.id, course_name=register_course_request.course_name, start_date_time=row.start_date_time, end_date_time=row.end_date_time, created= row.created)

async def add_course_grant(db: AsyncSession, registered_course:course_schema.RegisteredCourse, user_with_grant:UserWithGrant):
    new_course_grant = course_schema.CourseGrantCreate(user_id=user_with_grant.id,course_id=registered_course.id,start_date_time=datetime.datetime.now(),end_date_time=datetime.datetime.now()+datetime.timedelta(days=365),read_answer=True,update_answer=True,delete_answer=True)
    row = course_model.CourseGrant(**new_course_grant.dict())
    db.add(row)
    return

async def add_content(db: AsyncSession,content:str):
    new_content = content_schema.ContentCreate(content=content)
    row = content_model.Content(**new_content.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    content_id = row.id
    return content_id

async def add_block(db: AsyncSession,course_id,content_id,order):
    new_block = block_schema.BlockCreate(course_id=course_id,content_id=content_id,order=order)
    row = block_model.Block(**new_block.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    block_id = row.id
    return block_id

async def add_block_rules(db: AsyncSession,block_id,rules=None):
    new_block_rule = block_schema.BlockRuleCreate(block_id=block_id)
    if rules != None:
        if "start_date_time" in rules:
            new_block_rule.start_date_time = rules["start_date_time"]
        if "end_date_time" in rules:
            new_block_rule.start_date_time = rules["end_date_time"]
        if "always" in rules:
            new_block_rule.start_date_time = rules["always"]
    row = block_model.BlockRule(**new_block_rule.dict())
    db.add(row)
    return 

async def add_flow(db: AsyncSession,course_id,flow_dict):
    # コンテンツの登録
    welcome_page_content_id = await add_content(db,flow_dict["welcome_page_content"])
    completion_page_content_id = await add_content(db,flow_dict["completion_page_content"])
    new_flow = flow_schema.FlowCreate(course_id=course_id, title=flow_dict["title"], welcome_page_content_id= welcome_page_content_id, completion_page_content_id= completion_page_content_id)
    row = flow_model.Flow(**new_flow.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return row.id

async def add_flow_grant(db: AsyncSession,flow_id, user_id):
    new_flow_grant = flow_schema.FlowGrantCreate(user_id=user_id, flow_id=flow_id, start_date_time=datetime.datetime.now(), end_date_time=datetime.datetime.now()+datetime.timedelta(days=365), read_answer=True, update_answer=True, delete_answer=True)
    row = flow_model.FlowGrant(**new_flow_grant.dict())
    db.add(row)
    return

async def add_flow_rule(db: AsyncSession,flow_id, rules=None):
    new_flow_rule = flow_schema.FlowRule(flow_id=flow_id)
    if rules != None:
        if "check_answer_timing" in rules:
            new_flow_rule.check_answer_timing = rules["check_answer_timing"]
        if "challenge_limit" in rules:
            new_flow_rule.challenge_limit = rules["challenge_limit"]
        if "restart_session" in rules:
            new_flow_rule.restart_session = rules["restart_session"]
        if "time_limit" in rules:
            new_flow_rule.time_limit = rules["time_limit"]
        if "start_date_time" in rules:
            new_flow_rule.start_date_time = rules["start_date_time"]
        if "end_answer_date_time" in rules:
            new_flow_rule.end_answer_date_time = rules["end_answer_date_time"]
        if "end_read_date_time" in rules:
            new_flow_rule.end_read_date_time = rules["end_read_date_time"]
        if "check_answer_timing" in rules:
            new_flow_rule.check_answer_timing = rules["check_answer_timing"]
        if "always" in rules:
            new_flow_rule.always = rules["always"]
    row = flow_model.FlowRule(**new_flow_rule.dict())
    db.add(row)
    return

# async def add_flow_group(db: AsyncSession, flow_id,order,)

async def add_course_file(db: AsyncSession, user_with_grant:UserWithGrant, register_course_request:course_schema.RegisterCourseRequest,course_dict,flow_yml_list) -> course_schema.RegisterCourseResponse:
    # コースの追加
    registered_course = await add_course(db, register_course_request)
    # コース権限の追加
    await add_course_grant(db, registered_course, user_with_grant)

    # コースブロックの追加
    # コンテンツの登録
    if "content" in course_dict:
        content_id = await add_content(db, course_dict["content"])  # コンテンツの登録
        block_id = await add_block(db, course_id=registered_course.id,content_id=content_id,order=0)   # ブロックの登録
        await add_block_rules(db, block_id)
    # ブロックの登録
    else:
        for block_i, block in enumerate(course_dict["blocks"]):
            content_id = await add_content(db, block["content"])    # コンテンツの登録
            block_id = await add_block(db=db, course_id=registered_course.id,content_id=content_id,order=block_i) # ブロックの登録
            # ブロックルールの登録
            if "rules" in block:
                await add_block_rules(db=db, block_id=block_id,rules=block["rules"])
            else:
                await add_block_rules(db=db, block_id=block_id)

    # フローの追加
    for flow in flow_yml_list:
        flow_id = await add_flow(db,registered_course.id,flow)
        await add_flow_grant(db,flow_id,user_with_grant.id)
        if "rules" in flow:
            await add_flow_rule(db,flow_id,flow["rules"])
        else:
            await add_flow_rule(db,flow_id)

    await db.commit()
    return {"success":True,"error_msg":"","registered_course":registered_course}

async def register_course(user_with_grant:UserWithGrant, register_course_request:course_schema.RegisterCourseRequest,db: AsyncSession):
    yaml_formatter = YamlFormatter(register_course_request.course_files)
    validate_result = yaml_formatter.validate_files()
    if validate_result["success"]:
        result = await add_course_file(db, user_with_grant, register_course_request,yaml_formatter.course_yml_dict,yaml_formatter.flow_yml_list)
        return result
    return validate_result
