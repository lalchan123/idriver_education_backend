import os
import json

# global function
from FunctionFolder.WrapperFunc import *

def UIGETAPI1(user, api_name, paramList):

    if user == 'Sahak' and api_name == 'sahaknewapi':
        return 1+2



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

    

    if user == 'Sahak' and api_name == 'objectcodeapi2024' and  paramList:
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

    if user == 'Sahak' and api_name == 'objectapivalue2025' and  paramList:
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

    if user == 'lalchan' and api_name == 'cnbc_data_gq' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        if a > b :
        	if a==b:
        		return a +1
        	else:
        		return a+b
        else:
            return b - a 






    if user == 'Badsa' and api_name == 'api_sum' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        a = 30
        b = 40
        return a + b

    if user == 'Sahak' and api_name == 'demo api name852' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'TestdemoAAL' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return Daily_diff(a)

    if user == 'Badsa' and api_name == 'ccncnc' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        

    if user == 'Badsa' and api_name == 'Daily diff' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        
        return Daily_diff(a)

    if user == 'Sahak' and api_name == 'aabb' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return Daily_diff(a)

    if user == 'Sahak' and api_name == 'new apai' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'newapidata' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'fdsfsdfdsf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'fdsfsdfdsf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'dgdgdf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'dfdsfdfdf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'testapi' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return 52

    if user == 'Sahak' and api_name == 'dfdsfdfdf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'dfdsfdfdf' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b+c

    if user == 'Sahak' and api_name == 'demoapi' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'demoapi' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Sahak' and api_name == 'ssss' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a

    if user == 'Sahak' and api_name == 'ssss' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a*2

    if user == 'Badsa' and api_name == 'lalchan-rest-api' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        return a+b

    if user == 'Badsa' and api_name == 'fetch-16-03-24' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        def ABCSUM(a, b):
            if a>b:
              return a+b
            if a<b:
              print("minus",b-a)
              return b-a
              
        result=ABCSUM(a, b)

    if user == 'Badsa' and api_name == '16324lal1' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        def ABCSUM(a, b):
            if a>b:
              return a+b
            if a<b:
              print("minus",b-a)
              return b-a
              
        result=ABCSUM(a, b)

    if user == 'Badsa' and api_name == '16324lal2' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        def ABCSUM(a, b):
            if a>b:
              return a+b
            if a<b:
              print("minus",b-a)
              return b-a
              
        result=ABCSUM(a, b)

    if user == 'Badsa' and api_name == '19324api1' and  paramList:
        a=''
        b=''
        for key, values in paramList.items():
            if key == 'a':
                a = values
            if key == 'b':
                b = values

        def ABCSUM(a, b):
            if a>b:
              return a+b
            if a<b:
              print("minus",b-a)
              return b-a
              
        result=ABCSUM(a, b)

