from fastapi import  Depends,HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from typing import List, Optional, Tuple
import datetime

from api.schemas.user import UserWithGrant
import api.models.course as course_model
import api.models.content as content_model
import api.models.block as block_model
import api.models.flow as flow_model
import api.models.page_group as page_group_model
import api.models.flow_page as flow_page_model
import api.models.image as image_model


import api.schemas.content as content_schema
import api.schemas.block as block_schema
import api.schemas.course as course_schema
import api.schemas.flow as flow_schema
import api.schemas.page_group as page_group_schema
import api.schemas.flowpage as flow_page_schema
import api.schemas.image as image_schema

import yamale
import yaml
import traceback
import re
import uuid

class YamlFormatter():
    def __init__(self,files:List[course_schema.RegisterCourseRequest]):
        self.directory_structure = self.create_directry_structure(files)
        self.course_yml_dict = {}
        self.flow_yml_list = []
        self.image_dict = {}

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
                print(included_yml_with_indent)
                yml_text = re.sub(f'{script[0]}{{{{{script[1]}\s*\({script[2]}\)}}}}',included_yml_with_indent.replace("\\","\\\\"),yml_text)
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
            # imageリンクの存在チェック
            image_links = re.findall('\(\s*image\s*:\s*(.+?)\s*\)',yml_text,re.S)
            for link in image_links:
                if not link[0] in self.directory_structure[self.root_directory]["images"]:
                    validate_error += [f"image_file '{link[0]}' is not found."]
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
        
        ## image_dict {ファイル名：バイナリデータ}の追加
        course_validation_success = True
        if "images" in self.directory_structure[self.root_directory]:
            image_files = self.directory_structure[self.root_directory]["images"].keys()
            for image_name in image_files:
                if not re.match('.*\.(jpeg|jpg|png)$',image_name):
                    error_msg += f"{image_name} is not yml_file\n"
                image_data = self.directory_structure[self.root_directory]["images"][image_name]
                self.image_dict[image_name] = image_data.encode()
        
        
        ## 書き込み可否
        if course_validation_success and  course_validation_success:
            return {"success":True, "error_msg":error_msg}
        return {"success":False, "error_msg":error_msg}

async def add_course(db: AsyncSession, register_course_request:course_schema.RegisterCourseRequest, user_with_grant: UserWithGrant):
    new_course = course_schema.CourseCreate(course_name=register_course_request.course_name,start_date_time=register_course_request.start_date_time,end_date_time=register_course_request.end_date_time, created_by=user_with_grant.id)
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

async def add_image(db: AsyncSession, image_name: str, image_data: bytes):
    new_image = image_schema.ImageCreate(name=image_name, imgdata=image_data)
    row = image_model.Image(**new_image.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return row.id

async def add_flow(db: AsyncSession,course_id,flow_dict):
    # コンテンツの登録
    welcome_page_content_id = await add_content(db,flow_dict["welcome_page_content"])
    completion_page_content_id = await add_content(db,flow_dict["completion_page_content"])
    new_flow = flow_schema.FlowCreate(id_in_yml=flow_dict["id"], course_id=course_id, title=flow_dict["title"], welcome_page_content_id= welcome_page_content_id, completion_page_content_id= completion_page_content_id)
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
    new_flow_rule = flow_schema.FlowRuleCreate(flow_id=flow_id)
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

async def add_page_groups(db: AsyncSession, flow_id: int, order: int, page_group: dict):
    new_page_groups = page_group_schema.PageGroupCreate(flow_id=flow_id, order=order)
    if "shuffle" in page_group:
        new_page_groups.shuffle = page_group["shuffle"]
    if "num_of_show" in page_group:
        new_page_groups.num_of_show = page_group["num_of_show"]
    row = page_group_model.PageGroup(**new_page_groups.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return row.id

async def add_blank(db: AsyncSession, flowpage_id: int, blank_id: str):
    new_blank = flow_page_schema.BlankCreate(id=blank_id, flowpage_id=flowpage_id)
    row = flow_page_model.Blank(**new_blank.dict())
    db.add(row)
    return

async def add_correct_answer(db: AsyncSession, flowpage_id: int, blank_id: int, correct_answer: dict):
    new_correct_answer = flow_page_schema.CorrectAnswerCreate(flowpage_id=flowpage_id, blank_id=blank_id, type=correct_answer["type"], value=correct_answer["value"])
    row = flow_page_model.CorrectAnswer(**new_correct_answer.dict())
    db.add(row)
    return

async def add_simple_page(db: AsyncSession, content_id: int, flow_page: dict):
    # フローページを追加
    new_simple_page = flow_page_schema.PageCreate(content_id=content_id, title=flow_page["title"], page_type=flow_page["page_type"])
    row = flow_page_model.Page(**new_simple_page.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return row.id

async def add_single_text_question(db: AsyncSession, content_id: int, flow_page: dict):
    # フローページを追加
    new_single_text_question = flow_page_schema.SingleTextQuestionCreate(content_id=content_id, title=flow_page["title"], page_type=flow_page["page_type"])
    row = flow_page_model.SingleTextQuestion(**new_single_text_question.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    flowpage_id = row.id

    # 回答欄と正答の情報を追加
    blank_id = "blank_"+ str(uuid.uuid4())
    await add_blank(db=db, blank_id=blank_id, flowpage_id=flowpage_id)
    for correct_answer in flow_page["correct_answer"]:
        await add_correct_answer(db=db, flowpage_id=flowpage_id, blank_id=blank_id, correct_answer=correct_answer)
    return flowpage_id

async def add_multiple_text_question(db: AsyncSession, content_id: int, flow_page: dict):
    # フローページを追加
    answer_column_content_id = await add_content(db=db, content=flow_page["answer_column"])
    new_multiple_text_question = flow_page_schema.MultipleTextQuestionCreate(content_id=content_id, title=flow_page["title"], page_type=flow_page["page_type"], answer_column_content_id=answer_column_content_id)
    row = flow_page_model.MultipleTextQuestion(**new_multiple_text_question.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    flowpage_id = row.id
    
    # 回答欄と正答の情報を追加
    for correct_answer in flow_page["correct_answers"]:
        blank_id = correct_answer["blank_id"]
        await add_blank(db=db, blank_id=blank_id, flowpage_id=flowpage_id)
        for answer in correct_answer["answers"]:
            await add_correct_answer(db=db, flowpage_id=flowpage_id, blank_id=blank_id, correct_answer=answer)
    return flowpage_id

async def add_descriptive_text_question(db: AsyncSession, content_id: int, flow_page: dict):
    # フローページを追加
    new_descriptive_text_question = flow_page_schema.DescriptiveTextQuestionCreate(content_id=content_id, title=flow_page["title"], page_type=flow_page["page_type"])
    row = flow_page_model.DescriptiveTextQuestion(**new_descriptive_text_question.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    flowpage_id = row.id

    # 解答欄情報の追加
    blank_id = "blank_"+ str(uuid.uuid4())  # 仮のblank_idを生成
    await add_blank(db=db, blank_id=blank_id, flowpage_id=flowpage_id)
    return flowpage_id

async def add_choice_question_choices(db: AsyncSession, flowpage_id: int, order: int, choice: dict):
    content_id = await add_content(db=db, content=choice["choice_text"])
    new_choice_question_choices = flow_page_schema.ChoiceQuestionChoicesCreate(id=choice["choice_id"], flowpage_id=flowpage_id, order=order, content_id=content_id)
    row = flow_page_model.ChoiceQuestionChoice(**new_choice_question_choices.dict())
    db.add(row)
    return

async def add_choice_question(db: AsyncSession, content_id: int, flow_page: dict):
    # フローページを追加
    new_choice_question = flow_page_schema.ChoiceQuestionCreate(content_id=content_id, title=flow_page["title"], page_type=flow_page["page_type"])
    row = flow_page_model.ChoiceQuestion(**new_choice_question.dict())
    db.add(row)
    await db.flush()
    await db.refresh(row)
    flowpage_id = row.id

    # 選択肢情報の追加
    blank_id = "blank_"+ str(uuid.uuid4())  # 仮のblank_idを生成
    await add_blank(db=db, blank_id=blank_id, flowpage_id=flowpage_id)
    for choice_i, choice in enumerate(flow_page["choices"]):
        await add_choice_question_choices(db=db, flowpage_id=flowpage_id, order=choice_i, choice=choice)
    
    # 正答情報の追加
    for correct_choice_id in flow_page["correct_choices"]:
        correct_answer = {"type": "str", "value": correct_choice_id}
        await add_correct_answer(db=db, flowpage_id=flowpage_id, blank_id=blank_id, correct_answer=correct_answer)
    return flowpage_id

async def add_flow_page(db: AsyncSession, flow_page: dict):
    content_id = await add_content(db, flow_page["content"])
    page_type = flow_page["page_type"]
    if page_type in ["page","Page"]:
        return await add_simple_page(db=db, content_id=content_id, flow_page=flow_page)
    if page_type in ["single_text_question","SingleTextQuestion"]:
        return await add_single_text_question(db=db, content_id=content_id, flow_page=flow_page)
    if page_type in ["multiple_text_question","MultipleTextQuestion"]:
        return await add_multiple_text_question(db=db, content_id=content_id, flow_page=flow_page)
    if page_type in ["descriptive_text_question","DescriptiveTextQuestion"]:
        return await add_descriptive_text_question(db=db, content_id=content_id, flow_page=flow_page)
    if page_type in ["choice_question","ChoiceQuestion"]:
        return await add_choice_question(db=db, content_id=content_id, flow_page=flow_page)
    else:
        raise ValueError(f"page_type {page_type} is not defined.")

async def add_page_group_flow_pages(db: AsyncSession, page_group_id: int, flowpage_id: int, order: int):
    new_page_gruop_flowpages = page_group_schema.PageGroupFlowPagesCreate(pagegroup_id=page_group_id, flowpage_id=flowpage_id, order=order)
    row = page_group_model.PageGroupFlowPages(**new_page_gruop_flowpages.dict())
    db.add(row)
    return

async def add_course_file(db: AsyncSession, user_with_grant:UserWithGrant, register_course_request:course_schema.RegisterCourseRequest,course_dict,flow_yml_list,image_dict) -> course_schema.RegisterCourseResponse:
    # コースの追加
    registered_course = await add_course(db, register_course_request,user_with_grant)
    # コース権限の追加
    await add_course_grant(db, registered_course, user_with_grant)


    # 画像の追加
    id_in_image_name = {}
    for image_name,image_data in image_dict.items():
        image_id = await add_image(db, image_name, image_data)
        id_in_image_name[image_id] = image_name

    
    # フローの追加
    id_in_yml_flow_id_dict = {}
    for flow in flow_yml_list:
        flow_id = await add_flow(db,registered_course.id,flow)
        id_in_yml_flow_id_dict[flow["id"]] = flow_id
        print(f"flow_id: {flow_id}")
        await add_flow_grant(db,flow_id,user_with_grant.id)
        if "rules" in flow:
            await add_flow_rule(db,flow_id,flow["rules"])
        else:
            await add_flow_rule(db,flow_id)
        for page_group_i, page_group in enumerate(flow["page_groups"]):
            page_group_id = await add_page_groups(db=db, flow_id=flow_id, order=page_group_i, page_group=page_group)
            print(f"page_group_id: {page_group_id}")

            # ページの追加
            for page_i, page in enumerate(page_group["pages"]):
                flowpage_id = await add_flow_page(db=db, flow_page=page)
                # フローグループとページの対応情報を追加
                await add_page_group_flow_pages(db=db, page_group_id=page_group_id, flowpage_id=flowpage_id, order=page_i+1)

    # コースブロックの追加
    # コンテンツの登録
    for course_list in course_dict.values():
        for course_list_dict in course_list:
            if "content" in course_list_dict.keys():
                content = course_list_dict["content"]
                for id_in_yml, flow_id in id_in_yml_flow_id_dict.items():
                    content = re.sub(f"\(\s*flow/{id_in_yml}\s*\)", f"({registered_course.id}/flow/{flow_id})", content)
                # yml (image/image.jpg) -> markdawn ![~~](url)
                for image_id, image_name in id_in_image_name.items():
                    content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage](http://localhost:8000/get_image/{image_id})", content)
                content_id = await add_content(db, content)  # コンテンツの登録
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

    await db.commit()
    return {"success":True,"error_msg":"","registered_course":registered_course}

async def register_course(user_with_grant:UserWithGrant, register_course_request:course_schema.RegisterCourseRequest,db: AsyncSession):
    yaml_formatter = YamlFormatter(register_course_request.course_files)
    validate_result = yaml_formatter.validate_files()
    if validate_result["success"]:
        result = await add_course_file(db, user_with_grant, register_course_request,yaml_formatter.course_yml_dict,yaml_formatter.flow_yml_list,yaml_formatter.image_dict)
        return result
    return validate_result