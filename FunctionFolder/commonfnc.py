import os, json
import time
from datetime import datetime, timedelta, timezone

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)     

def dtm():
    now_utc = datetime.utcnow()
    now_utc1 = datetime.utcnow()+timedelta(minutes = 5)
    now_utc_5 = datetime.utcnow()-timedelta(minutes = 5)
    curdatetime = datetime.strftime(now_utc, '%Y-%m-%d %H:%M:%S')
    # curdatetime1 = datetime.strftime(now_utc, '%Y-%m-%d %H:%M:%S.%f').rstrip('0')
    curdate = datetime.strftime(now_utc, '%Y-%m-%d')
    curdate5 = datetime.strftime(now_utc1, '%Y-%m-%d %H:%M:%S')
    curdate_5 = datetime.strftime(now_utc_5, '%Y-%m-%d %H:%M:%S')
    sec = datetime.strftime(now_utc, '%S')
    curdatetimestamp = datetime.strptime(curdatetime, "%Y-%m-%d %H:%M:%S").timestamp()
    curdatestamp = datetime.strptime(curdate, "%Y-%m-%d").timestamp()
    curtimestamp5 = datetime.strptime(curdate5, "%Y-%m-%d %H:%M:%S").timestamp()
    curtimestamp_5 = datetime.strptime(curdate_5, "%Y-%m-%d %H:%M:%S").timestamp()

    return curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5

