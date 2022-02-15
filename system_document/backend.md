# APIルーティング

# DB構成
## Users
- id: int \<primary_key>
- username: str \<notnull>
- email: str \<unique, notnull>
- hashed_password: str \<notnull>
- is_active: bool \<notnull>
- created: datetime \<notnull>
- user_kind_id: int \<foreign_key\<UserKind.id>, notnull>

## UserKind
- id: int \<primary_key>
- kind_name: str \<notnull>
- create: boolean \<notnull>

## CourseGrant
\<primary_key= user_id, coure_id>
- user_id: int
- course_id: int
- start_date_time: datetime \<notnull>
- end_date_time: datetime \<notnull>
- read_answer: boolean \<notnull>
- update: boolean \<notnull>
- delete: boolean \<notnull>

## Contents
- id: int \<primary_key>
- created: datetime \<notnull>
- content: str

## TakingCourse
\<primary_key= user_id, coure_id>
- user_id: int \<foreign_key\<Users.id>>
- course_id: int \<foreign_key\<Courses.id>>

## Courses
- id: int \<primary_key>
- course_name: str \<notnull>
- created: datetime \<notnull>

## Blocks
- id: int \<primary_key>
- course_id: int \<foreign_key\<Courses.id>>
- content_id: int \<foreign_key\<Contents.id>>
- weight: int \<notnull>

## BlockRules
- block_id: int \<foreign_key\<Blocks.id>>
- start_date_time: datetime
- end_date_time: datetime
- always: boolean

## Flows
- id: str \<primary_key>
- title: str \<notnull>
- course_id: str \<foreign_key\<Courses.id>>
- created: datetime \<notnull>
- welcome_page_content_id: int \<foreign_key\<Contents.id>>
- completion_page_content_id: int \<foreign_key\<Contents.id>>

## FlowGrant
\<primary_key= user_id, flow_id>
- user_id: int
- flow_id: int
- start_date_time: datetime
- end_date_time: datetime
- read_answer: boolean \<notnull>
- update: boolean \<notnull>
- delete: boolean \<notnull>

## FlowRules
- flow_id: int \<foreign_key\<Flows.id>>
- check_answer_timing: str
- challenge_limit: int
- restart_session: bool
- time_limit: time 
- start_date_time: datetime 
- end_answer_date_time: datetime
- end_read_date_time: datetime
- always: boolean

## PageGroup
- id: int \<primary_key>
- flow_id: int \<foreign_key\<Flows.id>>
- order: int \<notnull>
- shuffle: Boolean
- num_of_show: int

## PageGroupFlowPages
\<primary_key= pagegroup_id, flowpage_id>
- pagegroup_id: int \<foreign_key\<PageGroup.id>>
- flowpage_id: int \<foreign_key\<FlowPage.id>>

## FlowPage
- id: int \<primary_key>
- content_id: int \<foreign_key\<Contents.id>>
- title: str \<notnull>
- created: datetime \<notnull>
- page_type: str \<notnull>

## Page
- flowpage_id: int \<foreign_key\<FlowPage.id>>

## Questions
- flowpage_id: int \<foreign_key\<FlowPage.id>>

## SingleTextQuestions
- flowpage_id: int \<foreign_key\<FlowPage.id>>

## MultipleTextQuestions
- flowpage_id: int \<foreign_key\<FlowPage.id>>
- answer_column_content_id : int \<foreign_key\<Contents.id>>

## DescriptiveTextQuestions
- flowpage_id: int \<foreign_key\<FlowPage.id>>

## ChoiceQuestions
- flowpage_id: int \<foreign_key\<FlowPage.id>>
- shuffle: bool \<notnull>

## ChoiceQuestionChoices
- id: int \<primary_key>
- flowpage_id: int \<foreign_key\<FlowPage.id>>
- order: int <notnull>
- content_id: str \<foreign_key\<Contents.id>>

## Blanks
- id: int \<primary_key>
- flowpage_id: int \<foreign_key\<Page.id>>

## CorrectAnswers
- id: int \<primary_key>
- flowpage_id : int
- blank_id: int \<foreign_key\<Blanks.id>>
- type: str \<notnull>
- value: str \<notnull>

## FlowSession
- id: int \<primary_key>
- user_id: int
- flow_id: int
- start_date_time: datetime
- finish_date_time: datetime
- is_finished: boolean

## FlowSessionFlowPages
- flow_session_id: int
- flowpage_id: int
- order: int
- submitted: boolean

## FlowSessionBlankAnswer
- flow_session_id: int
- flowpage_id: int
- blank_id: int
- answer: str
- created: datetime
