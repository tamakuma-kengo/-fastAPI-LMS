
# 構成要素の仕様
## Course
### Arguments
ContentかList\<Block>のいずれかを指定する
- title \<str> (Require)
- content: \<Content>
- blocks: \<List<\<Block>>

## Block
### Arguments
- title: \<str> (Require)
- rules: \<List\<BlockRules>>
- content: \<Content> (Require)

## BlockRules
### Arguments
- start_date_time: \<yyyy/mm/dd_hh/MM/dd>
    - Blockの表示を開始する日時
- end_date_time: \<yyyy/mm/dd_hh/MM/dd>
    - Blockの表示を終了する日時
- always: \<Boolean>
    - このBlockを常に表示するか. デフォルトはTrue. start_date_timeかend_date_timeが指定されるとこの値は無視される. 


## Flow
### Arguments
- title: \<str> (Require)
- welcome_page_content: \<Content> (Require)
    - Flowの最初のページの内容. 
- completion_page_content: \<Content> (Require)
    - Flowの最後のページの内容
- rules: \<List\<FlowRules>>>
    - Flowのルール
- page_gruops: \<List\<PageGroup>> (Require)
    - フローを構成するページを指定する. PageGroupのリストで指定し, PageGroupはグループ内でシャッフルなどの機能を提供する. 

## FlowRules
### Arguments
- check_answer_timing: ["None","submit_page","end_of_flow"]
    - 答え合わせをするタイミング
    - デフォルトは"submit_page"
    - "None": 答え合わせをしない
    - "submit_page": ページにある"Submit"ボタンを押すと解答を表示
    - "end_of_flow": フローの最終ページで答えを表示
- challenge_limit: int
    - フローに挑戦できる回数を指定
    - 指定しない場合は無制限に挑戦可能
    - 値は1以上の整数値
- restart_session: bool
    - 中断したセッションをリスタートできるか
    - デフォルトはTrue
- time_limit: \<HH:MM:SS>
    - Flowの時間制限を設定する. 
    - 指定しない場合は制限時間なし. 
- start_date_time: \<yyyy/mm/dd_hh/MM/dd>
    - Flowの表示を開始する日時
- end_answer_date_time: \<yyyy/mm/dd_hh/MM/dd>
    - Flowの回答を終了する日時
- end_read_date_time: \<yyyy/mm/dd_hh/MM/dd>
    - Flowの閲覧を終了する日時
- always: \<Boolean>
    - このFlowを常に表示するか. デフォルトはTrue. start_date_timeかend_date_timeが指定されるとこの値は無視される. 

## PageGroup
### Arguments
- pages: \<List\<Page>> (Require)
- shuffle: \<Boolean>
    - PageGroup内で表示順をシャッフルするかどうか. デフォルトはFalse.
- num_of_show: \<Integer>
    - PageGroup内で何個のページを表示するか. shuffleがTrueでないと例外を投げる. 

## Page
- ページを意味する親クラス. 子クラスには, [Page, Question] がある.
-  Flow -> PageGroup内にリストで指定する. 
### Arguments
- title: \<String>
- content: \<Content>
- page_type: \<String>

## Page.Page
### Arguments
- page_type:\<String> = "page"

## Page.Question
- Pageの子クラスであり, 問題を提供する. 
- 小クラスには, [SingleTextQuestion, MultipleTextQuestion, DescriptiveQuestion, ChoiceQuestion] がある. 
### Arguments
- なし

## CorrectAnswer
### Arguments
- blank_id: \<str>
    - 解答欄のid, 同じPage内でUnique
- answers: \<List\<Answer>>
    - 正答のリスト. 

## Answer
### Arguments
- type: \<str>
    - 回答の型. 型はpython準拠. 
- value: \<str>
    - 正答の値

## Page.Question.SigleTextQuestion
### Arguments
- page_type:\<String> = "SingleTextQuestion"
- correct_answer: \<CorrectAnswer>
    - 問題の正答を記述する. 

## Page.Question.MultipleTextQuestion
### Arguments
- page_type:\<String> = "MultipleTextQuestion"
- correct_answers: \<List\<CorrectAnswer>>
    - 問題の正答を記述する. 

## Page.Question.DescriptiveTextQuestion
### Arguments
- なし

## Page.Question.ChoiceQuestion
### Arguments
- page_type:\<String> = "ChoiceQuestion"
- correct_answer: \<CorrectAnswer>
    - 問題の正答を記述する. 
