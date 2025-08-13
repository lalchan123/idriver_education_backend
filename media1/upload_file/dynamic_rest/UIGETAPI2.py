
import os
import json

# global function
from FunctionFolder.WrapperFunc import *

def UIGETAPI2(user, api_name, paramList):
    
    if user == 'pervez' and api_name == 'cnbc_data_gq' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        a = 10
        b = 20
        if a > b :
            return a +b
        else:
            return b - a



