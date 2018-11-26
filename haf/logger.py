# encoding='utf-8'
import os
import time
import traceback
from multiprocessing import Process

from haf.busclient import BusClient

from haf.config import *


class Logger(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        self.bus_client = BusClient()
        while True:
            try:
                log_queue = self.bus_client.get_log()
                if log_queue.empty():
                    time.sleep(1)
                    continue
                log = log_queue.get()
                self.log_handler(log)
            except Exception as e:
                traceback.print_exc()

    def split_log(self, log):
        try:
            return log.rsplit("$%", 2)
        except Exception as ee:
            return f"log$%error$%{log}"

    def log_handler(self, log):
        temp1, temp2, msg = self.split_log(log)
        if "loader" in temp2:
            self.loader_handler(temp1, msg)
        elif "runner" in temp2:
            self.runner_handler(temp1, msg)
        elif "recorder" in temp2:
            self.recorder_handler(temp1, msg)
        elif "system" in temp2:
            self.system_handler(temp1, temp2, msg)
        elif "error" in temp2:
            self.error_handler(temp1, msg)
        else:
            self.case_handler(temp1, temp2, msg)

    def loader_handler(self,temp1, msg):
        self.write("loader", temp1, msg)

    def runner_handler(self, temp1, msg):
        self.write("runner", temp1, msg)

    def case_handler(self, temp1, temp2, msg):
        self.write(temp1, temp2, msg)

    def recorder_handler(self, temp1, msg):
        self.write("recorder", temp1, msg)

    def system_handler(self, temp1, temp2, msg):
        self.write("system", f"{temp1}.{temp2}", msg)

    def error_handler(self, temp1, msg):
        self.write("error", temp1, msg)

    def write(self, dir, filename, msg):
        dir = f"{LOG_PATH_DEFAULT}/{dir}"
        if not os.path.exists(dir):
            os.makedirs(dir)
        full_name = f"{dir}/{filename}.log"
        with open(full_name, 'a+') as f:
            f.write(f"{msg}\n")
            f.close()

    @property
    def now(self):
        '''
        get datetime now to str
        :return: time now str
        '''
        current_time = time.time()
        local_time = time.localtime(current_time)
        time_temp = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        secs = (current_time - int(current_time)) * 1000
        timenow = "%s %03d" % (time_temp, secs)
        return timenow

    def end_handler(self):
        result_handler = self.bus_client.get_result()
        result_handler.put(SIGNAL_RESULT_END)
        case_handler = self.bus_client.get_case()
        case_handler.put(SIGNAL_CASE_END)

