import pytest
import json
import datetime
from os import path
from pysjtu.schema import ScheduleCourseSchema, ScoreSchema, ScoreFactorSchema, ExamSchema, LibCourseSchema, GPAQueryParamsSchema, GPASchema
from pysjtu.model import LogicEnum, CourseRange, Ranking


@pytest.fixture()
def resp_loader():
    RESP_DIR = path.join(path.dirname(path.abspath(__file__)), 'resources/resp')

    def _resp_loader(name):
        with open(path.join(RESP_DIR, name + ".json")) as f:
            return json.load(f)

    return _resp_loader


def test_schedule_course_schema(resp_loader):
    raw_resp = resp_loader("schedule_course")
    schema = ScheduleCourseSchema()
    schedule_course = schema.load(raw_resp)

    assert schedule_course.name == "军事理论"
    assert schedule_course.day == 1 and isinstance(schedule_course.day, int)
    assert schedule_course.week == [6, 10, range(14, 16)]
    assert schedule_course.time == range(1, 3)
    assert schedule_course.location == "下院306"
    assert schedule_course.credit == 1.0 and isinstance(schedule_course.credit, float)
    assert schedule_course.assessment == "考试"
    assert schedule_course.remark == "无"
    assert schedule_course.teacher_name == ["闫成"]
    assert schedule_course.teacher_title == ["讲师(高校)"]
    assert schedule_course.course_id == "TH004"
    assert schedule_course.class_name == "(2019-2020-1)-TH004-2"
    assert schedule_course.class_id == "90BEF7AA5D657072E0530200A8C06959"
    assert schedule_course.hour_total == 16 and isinstance(schedule_course.hour_total, int)
    assert schedule_course.hour_remark == {"理论": 24, "其他": 24}
    assert schedule_course.hour_week == 1 and isinstance(schedule_course.hour_week, int)
    assert schedule_course.field == "无方向"


def test_score_factor_schema(resp_loader):
    raw_resp = resp_loader("score_factor")
    schema = ScoreFactorSchema(many=True)
    score_factors = schema.load(raw_resp)

    assert score_factors[0].name == "平时"
    assert score_factors[0].percentage == 0.4
    assert score_factors[0].score == 93 and isinstance(score_factors[0].score, float)

    assert score_factors[1].name == "期末"
    assert score_factors[1].percentage == 0.6
    assert score_factors[1].score == 90 and isinstance(score_factors[0].score, float)


def test_score_schema(resp_loader):
    raw_resp = resp_loader("score")
    schema = ScoreSchema()
    score = schema.load(raw_resp)

    assert score.name == "大学化学"
    assert score.teacher == "麦亦勇"
    assert score.score == "91"
    assert score.credit == 2 and isinstance(score.gp, float)
    assert score.gp == 4.0 and isinstance(score.gp, float)
    assert not score.invalid and isinstance(score.invalid, bool)
    assert score.course_type == "主修"
    assert score.category == "个性化教育课程"
    assert score.score_type == "正常考试"
    assert score.method == "考试"
    assert score.course_id == "CA001"
    assert score.class_name == "(2019-2020-1)-CA001-10"
    assert score.class_id == "90DD3334A9410650E0530200A8C03235"


def test_exam_schema(resp_loader):
    raw_resp = resp_loader("exam")
    schema = ExamSchema()
    exam = schema.load(raw_resp)

    assert exam.name == "2019-2020-1数学期中考"
    assert exam.location == "东上院509"
    assert exam.seat == 1
    assert exam.course_id == "MA248"
    assert exam.course_name == "高等数学I"
    assert exam.class_name == "(2019-2020-1)-MA248-7"
    assert not exam.rebuild and isinstance(exam.rebuild, bool)
    assert exam.credit == 6.0 and isinstance(exam.credit, float)
    assert not exam.self_study and isinstance(exam.self_study, bool)
    assert exam.date == datetime.date(2019, 11, 6)
    assert exam.time == [datetime.time(13, 10), datetime.time(15, 10)]


def test_gpa_query_params_schema_load(resp_loader):
    raw_resp = resp_loader("gpa_query_params")
    schema = GPAQueryParamsSchema()
    gpa_query_params = schema.load(raw_resp)

    assert gpa_query_params.gp_round == 9
    assert gpa_query_params.gpa_round == 9
    assert gpa_query_params.exclude_gp == "缓考"
    assert gpa_query_params.exclude_gpa == "缓考"
    assert gpa_query_params.course_whole == ["TH020", "TH009"]
    assert gpa_query_params.has_roll and isinstance(gpa_query_params.has_roll, bool)
    assert gpa_query_params.registered is None
    assert gpa_query_params.attending and isinstance(gpa_query_params.attending, bool)


def test_gpa_query_params_schema_dump(resp_loader):
    raw_resp = resp_loader("gpa_query_params")
    schema = GPAQueryParamsSchema()
    gpa_query_params = schema.load(raw_resp)

    gpa_query_params.end_term = 2019

    gpa_query_params.condition_logic = 0
    with pytest.raises(TypeError):
        schema.dump(gpa_query_params)
    gpa_query_params.condition_logic = LogicEnum.AND

    gpa_query_params.makeup_as_60 = True
    gpa_query_params.rebuild_as_60 = True

    gpa_query_params.course_range = 0
    with pytest.raises(TypeError):
        schema.dump(gpa_query_params)
    gpa_query_params.course_range = CourseRange.ALL

    gpa_query_params.ranking = 0
    with pytest.raises(TypeError):
        schema.dump(gpa_query_params)
    gpa_query_params.ranking = Ranking.GRADE_AND_FIELD

    gpa_query_params.has_roll = False
    gpa_query_params.registered = True
    gpa_query_params.attending = None

    dump_dict = schema.dump(gpa_query_params)

    assert dump_dict == {'zczt': 1, 'bjjd': '缓考', 'xjzt': 0, 'bjpjf': '缓考', 'qsXnxq': '', 'tjfw': 'njzy', 'kch_ids': 'TH020,TH009', 'sspjfblws': 9, 'tjgx': 0, 'pjjdblws': 9, 'zzXnxq': 2019, 'kcfw': 'qbkc', 'alsfj': 'bkcx'}


def test_lib_course_schema_1(resp_loader):
    schema = LibCourseSchema()
    raw_resp = resp_loader("lib_course_1")
    lib_course = schema.load(raw_resp)

    assert lib_course.name == "高等数学I"
    assert lib_course.day == 1 and isinstance(lib_course.day, int)
    assert lib_course.week == [range(1, 17)]
    assert lib_course.time == range(1, 3)
    assert lib_course.location == "东下院415"
    assert lib_course.locations == ["东下院415", "东下院415", "东下院415"]
    assert lib_course.faculty == "数学科学学院"
    assert lib_course.credit == 6.0 and isinstance(lib_course.credit, float)
    assert lib_course.teacher == ["王铭"]
    assert lib_course.course_id == "MA248"
    assert lib_course.class_name == "(2019-2020-1)-MA248-10"
    assert lib_course.class_id == "908698F1AEF44587E0530200A8C0E301"
    assert lib_course.class_composition == ["F1902122", "F1902123", "F1902127", "F1902142"]
    assert lib_course.hour_total == 96 and isinstance(lib_course.hour_total, int)
    assert lib_course.hour_remark == {"理论": 6.0}
    assert lib_course.seats == 168
    assert lib_course.students_elected == 100
    assert lib_course.students_planned == 115


def test_lib_course_schema_2(resp_loader):
    schema = LibCourseSchema()
    raw_resp = resp_loader("lib_course_2")
    lib_course = schema.load(raw_resp)

    assert lib_course.name == "高等数学A1"
    assert lib_course.day == 1 and isinstance(lib_course.day, int)
    assert lib_course.week == [range(1, 14, 2)]
    assert lib_course.time == range(1, 3)
    assert lib_course.location == "东下院102"
    assert lib_course.locations == ["东下院102", "东上院101", "上院100"]
    assert lib_course.faculty == "密西根学院"
    assert lib_course.credit == 4.0 and isinstance(lib_course.credit, float)
    assert lib_course.teacher == ["OLGA DANILKINA"]
    assert lib_course.course_id == "VV156"
    assert lib_course.class_name == "(2019-2020-1)-VV156-1"
    assert lib_course.class_id == "895A258003C03F72E0530200A8C0E75F"
    assert lib_course.class_composition == ["2019电子与计算机工程", "2019机械类"]
    assert lib_course.hour_total == 56 and isinstance(lib_course.hour_total, int)
    assert lib_course.hour_remark == {"理论": 4.0, "实验": 1.0}
    assert lib_course.seats == 126
    assert lib_course.students_elected == 113
    assert lib_course.students_planned == 300
