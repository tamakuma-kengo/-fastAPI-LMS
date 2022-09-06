from sqlalchemy.ext.asyncio import AsyncSession

import api.models.url_links as url_links_model

def add_url_links(db:AsyncSession):
    rows = [
            url_links_model.URLLinks(
                id = 1,
                week_id = 1,
                study_name = "数列の和とその極限",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/suuretu/henkan-tex.cgi?target=/math/category/suuretu/index.html"
            ),
            url_links_model.URLLinks(
                id = 2,
                week_id = 2,
                study_name = "リーマン和",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/teisekibun-no-teigi-2.html"
            ),
            url_links_model.URLLinks(
                id = 3,
                week_id = 2,
                study_name = "定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/teisekibun-no-kihonsiki.html"
            ),
            url_links_model.URLLinks(
                id = 4,
                week_id = 3,
                study_name = "不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/futeisekibun-no-kihonsiki.html"
            ),
            url_links_model.URLLinks(
                id = 5,
                week_id = 3,
                study_name = "微分積分学の基本定理",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/teisekibun-no-teigi.html"
            ),
            url_links_model.URLLinks(
                id = 6,
                week_id = 3,
                study_name = "べき関数の不定積分１",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-x^a.html"
            ),
            url_links_model.URLLinks(
                id = 7,
                week_id = 3,
                study_name = "べき関数の不定積分２",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-x^-1.html"
            ),
            url_links_model.URLLinks(
                id = 8,
                week_id = 4,
                study_name = "指数関数の不定積分１",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-e^x.html"
            ),
            url_links_model.URLLinks(
                id = 9,
                week_id = 4,
                study_name = "指数関数の不定積分２",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-a^x.html"
            ),
            url_links_model.URLLinks(
                id = 10,
                week_id = 4,
                study_name = "三角関数sinの不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-sinx.html"
            ),
            url_links_model.URLLinks(
                id = 11,
                week_id = 4,
                study_name = "三角関数cosの不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-cosx.html"
            ),
            url_links_model.URLLinks(
                id = 12,
                week_id = 4,
                study_name = "三角関数sec^2の不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-sec^2x.html"
            ),
            url_links_model.URLLinks(
                id = 13,
                week_id = 4,
                study_name = "三角関数csc^2の不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-cosec^2x.html"
            ),
            url_links_model.URLLinks(
                id = 14,
                week_id = 4,
                study_name = "その他の三角関数の不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/example/henkan-tex.cgi?target=/math/category/sekibun/example/sankakukansuu-exampke.html"
            ),
            url_links_model.URLLinks(
                id = 15,
                week_id = 4,
                study_name = "分数式の不定積分１",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-sonota_2.html"
            ),
            url_links_model.URLLinks(
                id = 16,
                week_id = 4,
                study_name = "分数式の不定積分２",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/example/henkan-tex.cgi?target=/math/category/sekibun/example/int-frac(1)(a%5E2_plus_x%5E2).html"
            ),
            url_links_model.URLLinks(
                id = 17,
                week_id = 4,
                study_name = "分数式の不定積分３",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/basic-int/henkan-tex.cgi?target=/math/category/sekibun/basic-int/int-sonota_3.html"
            ),
            url_links_model.URLLinks(
                id = 18,
                week_id = 5,
                study_name = "部分積分法",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/bubunsekibun.html"
            ),
            url_links_model.URLLinks(
                id = 19,
                week_id = 5,
                study_name = "ワリスの公式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/example/henkan-tex.cgi?target=/math/category/sekibun/example/int-(sinx)^n.html"
            ),
            url_links_model.URLLinks(
                id = 20,
                week_id = 6,
                study_name = "置換積分法",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/chikansekibun.html"
            ),
            url_links_model.URLLinks(
                id = 21,
                week_id = 7,
                study_name = "微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/kai.html"
            ),
            url_links_model.URLLinks(
                id = 22,
                week_id = 7,
                study_name = "変数分離形",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/hensuubunrikei.html"
            ),
            url_links_model.URLLinks(
                id = 23,
                week_id = 10,
                study_name = "1階線形微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/ikkai_senkei_bibun_eq.html"
            ),
            url_links_model.URLLinks(
                id = 24,
                week_id = 11,
                study_name = "2階線形同時微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/nikai_sennkei_douji.html"
            ),
            url_links_model.URLLinks(
                id = 25,
                week_id = 11,
                study_name = "定数係数の2階線形同時微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/nikaiteisuukeisuu_no_kai.html"
            ),
            url_links_model.URLLinks(
                id = 26,
                week_id = 15,
                study_name = "曲線の長さ",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/kyokusen-no-nagasa.html"
            ),
            url_links_model.URLLinks(
                id = 27,
                week_id = 15,
                study_name = "パラメータ表示（極座標）について",
                urls = "http://nakira.etc.kanazawa-it.ac.jp/math/physics/category/others/coordinates/henkan-tex.cgi?target=/math/physics/category/others/coordinates/circular_coordinates.html"
            ),
            url_links_model.URLLinks(
                id = 28,
                week_id = 16,
                study_name = "仕事",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/work/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/work/work.html"
            ),
            url_links_model.URLLinks(
                id = 29,
                week_id = 16,
                study_name = "仕事率",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/work/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/work/power.html"
            ),
            url_links_model.URLLinks(
                id = 30,
                week_id = 16,
                study_name = "運動エネルギー",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/energy/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/energy/kinetic_energy.html"
            ),
            url_links_model.URLLinks(
                id = 31,
                week_id = 17,
                study_name = "ポテンシャルエネルギー（位置エネルギー）",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/energy/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/energy/gravitational_potential_energy.html"
            ),
            url_links_model.URLLinks(
                id = 32,
                week_id = 17,
                study_name = "力学的エネルギー保存の法則",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/energy/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/energy/law_of_conservation_of_energy.html"
            ),
            url_links_model.URLLinks(
                id = 33,
                week_id = 17,
                study_name = "垂直抗力",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/force/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/force/normal_force.html"
            ),
            url_links_model.URLLinks(
                id = 34,
                week_id = 17,
                study_name = "動摩擦力",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/force/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/force/kinetic_friction_force.html"
            ),
            url_links_model.URLLinks(
                id = 35,
                week_id = 17,
                study_name = "運動量",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/momentum/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/momentum/momentum.html"
            ),
            url_links_model.URLLinks(
                id = 36,
                week_id = 17,
                study_name = "力積と運動量",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/momentum/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/momentum/impulse_momentum.html"
            ),
            url_links_model.URLLinks(
                id = 37,
                week_id = 17,
                study_name = "運動量保存の法則",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/momentum/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/momentum/law_of_conservation_of_momentum.html"
            ),
            url_links_model.URLLinks(
                id = 38,
                week_id = 17,
                study_name = "反発係数",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/momentum/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/momentum/coefficient_of_restitution_2.html"
            ),
            url_links_model.URLLinks(
                id = 39,
                week_id = 19,
                study_name = "図形の面積",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/henkan-tex.cgi?target=/math/category/sekibun/menseki-sekibun.html"
            ),
            url_links_model.URLLinks(
                id = 40,
                week_id = 20,
                study_name = "重積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/zyuusekibun/henkan-tex.cgi?target=/math/category/sekibun/zyuusekibun/zyuusekibun-kosiki.html"
            ),
            url_links_model.URLLinks(
                id = 41,
                week_id = 20,
                study_name = "変数変換（極座標など）の重積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/zyuusekibun/henkan-tex.cgi?target=/math/category/sekibun/zyuusekibun/hensuuhenkan.html"
            ),
            url_links_model.URLLinks(
                id = 42,
                week_id = 22,
                study_name = "体積",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/zyuusekibun/henkan-tex.cgi?target=/math/category/sekibun/zyuusekibun/taiseki-kyokumenseki.html"
            ),
            url_links_model.URLLinks(
                id = 43,
                week_id = 23,
                study_name = "運動エネルギー（復習）",
                urls = "https://w3e.kanazawa-it.ac.jp/math/physics/high-school_index/mechanics/energy/henkan-tex.cgi?target=/math/physics/high-school_index/mechanics/energy/kinetic_energy.html"
            ),
            url_links_model.URLLinks(
                id = 44,
                week_id = 23,
                study_name = "回転軸周りの慣性モーメント（z軸の慣性能率）",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/zyuusekibun/henkan-tex.cgi?target=/math/category/sekibun/zyuusekibun/zyuusekibun-ouyou.html"
            ),
            url_links_model.URLLinks(
                id = 45,
                week_id = 1,
                study_name = "復習問題：数列とその和",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/suuretu/question/henkan-tex.cgi?target=/math/category/suuretu/question/index.html"
            ),
            url_links_model.URLLinks(
                id = 46,
                week_id = 1,
                study_name = "復習問題：極限",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/other/kyokugen/question/henkan-tex.cgi?target=/math/category/other/kyokugen/question/index.html"
            ),
            url_links_model.URLLinks(
                id = 47,
                week_id = 1,
                study_name = "復習問題：数列の極限",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/ikkai_senkei_bibun_eq.html"
            ),
            url_links_model.URLLinks(
                id = 48,
                week_id = 2,
                study_name = "復習問題：定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/cgi-bin/question_list/question_list.cgi?node=/math/category/sekibun/teisekibun-no-kihonsiki.html"
            ),
            url_links_model.URLLinks(
                id = 49,
                week_id = 3,
                study_name = "復習問題：不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/cgi-bin/question_list/question_list.cgi?node=/math/category/sekibun/futeisekibun-no-kihonsiki.html"
            ),
            url_links_model.URLLinks(
                id = 50,
                week_id = 3,
                study_name = "復習問題：定積分・不定積分",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/sekibun/question/henkan-tex.cgi?target=/math/category/sekibun/question/sekibun-q.html"
            ),
            url_links_model.URLLinks(
                id = 51,
                week_id = 5,
                study_name = "復習問題：部分積分法",
                urls = "https://w3e.kanazawa-it.ac.jp/math/cgi-bin/question_list/question_list.cgi?node=/math/category/sekibun/bubunsekibun.html"
            ),  
            url_links_model.URLLinks(
                id = 52,
                week_id = 6,
                study_name = "復習問題：置換積分法",
                urls = "https://w3e.kanazawa-it.ac.jp/math/cgi-bin/question_list/question_list.cgi?node=/math/category/sekibun/chikansekibun.html"
            ),   
            url_links_model.URLLinks(
                id = 53,
                week_id = 7,
                study_name = "復習問題：微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/question/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/question/bibun-eq-q_2.html"
            ),   
            url_links_model.URLLinks(
                id = 54,
                week_id = 10,
                study_name = "復習問題：1階線形微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/question/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/question/bibun-eq-q_4.html"
            ),   
            url_links_model.URLLinks(
                id = 55,
                week_id = 11,
                study_name = "復習問題：1階線形微分方程式",
                urls = "https://w3e.kanazawa-it.ac.jp/math/category/bibun/bibunhouteisiki/question/henkan-tex.cgi?target=/math/category/bibun/bibunhouteisiki/question/bibun-eq-q_4.html"
            ),   
        ]
    for row in rows:
        db.add(row)
    db.flush()
