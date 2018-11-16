# encoding='utf-8'
import time
from multiprocessing import Process

from haf.apihelper import Request
from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.result import HttpApiResult
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils

logger = Log.getLogger(__name__)

class Runner(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.bus_client = None

    def load(self):
        pass

    def run(self):
        logger.debug("start runner {} ".format(self.pid))
        self.bus_client = BusClient()
        while True:
            case_handler = self.bus_client.get_case()
            if not case_handler.empty() :
                case = case_handler.get()
                logger.debug("runner {} -- get {}".format(self.pid, case))
                if isinstance(case, HttpApiCase):
                    result = self.run_case(case)
                    result_handler = self.bus_client.get_result()
                    result_handler.put(result)
                elif case == SIGNAL_CASE_END:
                    self.end_handler()
                    break
            time.sleep(0.1)

    def run_case(self, case):
        result = HttpApiResult()
        try:
            if isinstance(case, HttpApiCase):
                temp = ApiRunner.run(case)
                result.result = temp
            return result
        except Exception as e:
            logger.error(e)
            result.result = e
            return result

    def end_handler(self):
        logger.debug("end runner {} ".format(self.pid))
        result_handler = self.bus_client.get_result()
        result_handler.put(SIGNAL_RESULT_END)
        case_handler = self.bus_client.get_case()
        case_handler.put(SIGNAL_CASE_END)




class ApiRunner(object):

    @staticmethod
    def run(case:HttpApiCase):
        case.response = ApiRunner.request(case.request)

    @staticmethod
    def request(request:Request):
        Utils.http_request(request)
