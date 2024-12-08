
import json, os
import requests
from accountapp.classbase import GlobalJson
from FunctionFolder.UserConfig import *
from FunctionFolder.WrapperFunc import *
from accountapp.DynamicFunction.Process_Log import *
from accountapp.DynamicFunction.WebScrappingJson import *
from accountapp.DynamicFunction.LinkedList import *
from accountapp.DynamicFunction.JsonSelect import *
from accountapp.DynamicFunction.SentimentAnalyzer import *
from accountapp.DynamicFunction.ValidatorF import *
from media.upload_file.dynamic_rest.UIGETAPI1 import *
from media.upload_file.dynamic_rest.UIGETAPI2 import *
from media.upload_file.dynamic_rest.UIPOSTAPI import *
from media.upload_file.dynamic_rest.Custom import *
from media.upload_file.dynamic_rest.Custom2 import *



class ApiCodeRun:
    api_code_result = {}
    def __init__(self, item_data, paramList):
        self.item_data=item_data
        self.paramList=paramList

        g_obj = GlobalJson(main_media_url+f'/media/upload_file/investing/json/global_parameter.json')
        global_parameter=g_obj.var1

        print("paramList", paramList)

        for key, values in paramList.items():
            fileName = main_media_url+f'/media/upload_file/investing/json/pipelineapicreatecode.json'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['data']

                dataT = [x for x in array_data if x['api_name'] == values]
                print("39 dataT", dataT)

                if len(dataT)!=0:
                    # print("api_url", main_url+dataT[0]['api_url'], dataT[0]['paramList'])
                    r = requests.post(url=main_url+dataT[0]['api_url'], json=dataT[0]['paramList'])
                    # print("45 r", r.json()['data']['result'])
                    paramList[key]=r.json()['data']['result']
               

        print("57 paramList", paramList)        
         
        fileName = main_media_url+f'/media/upload_file/investing/json/pipelineapicreatecode.json'
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']

            for id in self.item_data:
                item_arr_data = [x for x in array_data if x['api_name'] == id['api_name'] and x['user'] == id['user'] and x['api_url'] == id['api_url'] and x['api_method'] == id['api_file'] and x['api_data_fetch_type'] == id['api_data_fetch_type']] 
                print("item_arr_data", item_arr_data)

                for m in item_arr_data:
                    loc = self.paramList
                    globals = eval(global_parameter)
                    exec(m['code'], globals, loc) 
                    print("42")
                    self.api_code_result['result']=loc['result']
    