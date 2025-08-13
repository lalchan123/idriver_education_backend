
import json
import os
import requests

from FunctionFolder.WrapperFunc import *

def Custom(job_name):
    # fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/code.json'
    # if os.path.isfile(fileName):
    #     f = open(fileName)
    #     data = json.load(f)
    #     array_data = data['data']

    #     for m in array_data:
    #         if m['job_name'] == job_name:
    #             exec(m['code'])
    
    url = f"https://itb-usa.a2hosted.com/account/job-data/{job_name}/"
    r = requests.get(url=url)
    
    for m in r.json()['job_data']:
        if m['job_name'] == job_name:
            exec(m['code'])
