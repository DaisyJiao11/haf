# encoding='utf-8'

from haf.config import *
from haf.utils import Utils


class BaseResult(object):
    def __init__(self):
        self.message_type = MESSAGE_TYPE_RESULT
        self._init_all()

    def _init_all(self):
        self.begin_time = None
        self.end_time = None
        self.result = None
        self.duration = 0
        self.passed = 0
        self.failed = 0
        self.skip = 0
        self.error = 0


class HttpApiResult(BaseResult):
    def __init__(self):
        super().__init__()
        self.message_type = MESSAGE_TYPE_RESULT
        self._init_all()

    def _init_all(self):
        self.case = None
        self.result_check_response = []
        self.result_check_sql_response = False
        self.run_error = None
        self.result = False
        self.begin_time = None
        self.end_time = None

    def on_case_begin(self):
        self.begin_time = Utils.get_datetime_now()

    def on_case_end(self):
        self.end_time = Utils.get_datetime_now()

    def deserialize(self):
        return {
            "case_name": f"{self.case.ids.id}.{self.case.ids.subid}.{self.case.ids.name}",
            "result_check_response": self.result_check_response,
            "result_check_sql_response": self.result_check_sql_response,
            "run_error": self.run_error,
            "result": RESULT_GROUP.get(str(self.result)),
            "begin_time": self.begin_time,
            "end_time": self.end_time,
            "case": self.case.deserialize()
        }


class Detail(object):
    def __init__(self, suite_name):
        self.suite_name = suite_name
        self.begin_time = ""
        self.end_time = ""
        self.duration = 0
        self.cases = []

    def deserialize(self):
        return {
            "suite_name":self.suite_name,
            "begin_time":self.begin_time,
            "end_time":self.end_time,
            "duration":self.duration,
            "cases": [
                x.deserialize() for x in self.cases
            ]
        }


class EndResult(BaseResult):

    def __init__(self, name:str=""):
        super().__init__()
        self.begin_time = ""
        self.end_time = ""
        self.duration = 0
        self.passed = 0
        self.failed = 0
        self.skip = 0
        self.error = 0
        self.all = 0
        self.suite_name = []
        self.summary = {}
        self.details = {}
        self.name = name
        self.version = PLATFORM_VERSION
        self.platform = Utils.get_platform()

    def deserialize(self):
        return {
            "begin_time":self.begin_time,
            "end_time":self.end_time,
            "duration":self.duration,
            "passed":self.passed,
            "failed":self.failed,
            "skip":self.skip,
            "error":self.error,
            "suite_name":self.suite_name,
            "summary": self.summary,
            "version": self.version,
            "name": self.name,
            "platform": self.platform,
            "details": [
                self.details.get(x).deserialize() for x in self.details.keys()
            ]
        }