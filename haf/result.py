# encoding='utf-8'

from haf.config import *
from haf.utils import *

class BaseResult(object):
    def __init__(self):
        self.message_type = MESSAGE_TYPE_RESULT
        self._init_all()

    def _init_all(self):
        self.begin_time = None
        self.end_time = None
        self.use_time = None
        self.result = None


class HttpApiResult(BaseResult):
    def __init__(self):
        super().__init__()
        self.message_type = MESSAGE_TYPE_RESULT
        self._init_all()

    def _init_all(self):
        self.sql = None
        self.case = None
        self.result_check_response = False
        self.result_check_sql_response = False

    def on_case_begin(self):
        self.begin_time = Utils.get_datetime_now()

    def on_case_end(self):
        self.end_time = Utils.get_datetime_now()


