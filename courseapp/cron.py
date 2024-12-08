import time
from datetime import datetime, timedelta

from django.conf import settings 

from accountapp.DynamicFunction.Process_Log import ProcessLogFunction, HeartBeatFunction
from courseapp.Scheduler.Casual import QueueFunction
from media.upload_file.process.CNBC import *



def job_start():
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    HeartBeatFunction(response_time=currenttimedate, server_name="Server1", status="Running")
    QueueFunction()
    # CNBC()
    # ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file="", log_data_type="cnbc", log_process_name="cnbc created", error="")

