import requests
import time
from datetime import datetime, timedelta

from FunctionFolder.UserConfig import *

def ChangeLogFunction(folder_path, api_url):
    url = main_url+"/account/change-log/"
    process_data = {
        "folder_path": folder_path,
        "api_url": api_url,
    }
    r = requests.post(url=url, data=process_data)  