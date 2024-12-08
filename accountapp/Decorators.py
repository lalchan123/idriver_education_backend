from django.core.cache import cache
import os, json
import time
from datetime import datetime, timedelta, timezone
from courseapp.models import *
from FunctionFolder.UserConfig import *
from FunctionFolder.commonfnc import *
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from FunctionFolder.GlobalFunction import *





# class UserLogin(object):
#     def __init__(self, arg1, arg2):
#         self.arg1 = arg1
#         self.arg2 = arg2

#     def __call__(self, original_func):
#         decorator_self = self

#         def wrappee( *args, **kwargs):
#             print("before")
#             original_func(*args,**kwargs)
#             print("before")
#         return wrappee

def JsonConvertData(df):
    try:
        DataItem = []
        KeyItem = []
        sections={}
        for key, value in df.iteritems():
            KeyItem.append(key)

        for index, row in df.iterrows():

            for i in range(len(KeyItem)):
                sections[KeyItem[i]]= row[KeyItem[i]]
            if sections != "":
                DataItem.append(sections)
                sections={}

        return DataItem
    
    except Exception as err:
        print("err", err)


def UserAPILogJsonFile(fileName, DataList):
    print("26", DataList)
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']
    
        for i in DataList:
            print("33")
            if len(news_array_data)!=0:
                print("34")
                compareValue = [x for x in news_array_data if x['time'][:10] == i['time'][:10] and x['api_url'] == i['api_url']]
                print("35")
                if len(compareValue)!=0:
                    for j in range(len(news_array_data)):
                        if news_array_data[j]['time'][:10] == i['time'][:10] and news_array_data[j]['api_url'] == i['api_url']:
                            news_array_data[j]['user_id'] = i['user_id']
                            news_array_data[j]['api_url'] = i['api_url']
                            news_array_data[j]['time'] = i['time']
                            news_array_data[j]['status'] = i['status']
                            news_array_data[j]['count'] += int(i['count'])
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=news_array_data
                                json.dump(file_data, file, indent=4)

                else:
                    print("35")
                    def write_json(new_data, filename=fileName):
                        with open(filename, 'r+') as file:
                            file_data = json.load(file)
                            file_data["data"].append(new_data)
                            file.seek(0)
                            json.dump(file_data, file, indent=4)
                    y = {
                        "user_id": i['user_id'],
                        "api_url": i['api_url'],
                        "time": i['time'],
                        "status": i['status'],
                        "count": i['count']
                    }

                    write_json(y)

            else:
                print("69")
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "user_id": i['user_id'],
                    "api_url": i['api_url'],
                    "time": i['time'],
                    "status": i['status'],
                    "count": i['count']
                }

                write_json(y)

    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": DataList
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)

def UserLogin(apikey, api_url):
   try:
        print("apikey", type(apikey))
        api_key_detail = Table_data_info.objects.get(table_id=2, table_col_id=4,  column_data=apikey,  column_name='user_token')
        # print("api_key_detail", api_key_detail)
        if api_key_detail:
            curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()

            fileName = main_media_url+f'/media/upload_file/investing/json/user_api_log.json'
            print("fileName", fileName)

            user_profile_data = Table_data_info.objects.get(table_id=630, table_col_id=2,  column_data=api_url,  column_name='api_url', user_id=api_key_detail.user_id)
            user_profile_permission_detail = Table_data_info.objects.filter(table_id=630, table_ref_id=user_profile_data.table_ref_id, user_id=user_profile_data.user_id)
            user_profile = {}
            for m in user_profile_permission_detail:
                user_profile['user_id'] = m.user_id
                user_profile[m.column_name] = m.column_data

            print("user_profile", user_profile)    
            f = open(fileName)
            data = json.load(f)
            news_array_data = data['data']

            filter_data = [x for x in news_array_data if x['user_id'] == user_profile['user_id'] and x['api_url'] == api_url]
            print("filter_data", filter_data)
            if user_profile['frequency'] == 'Daily':
                if len(filter_data) !=0:
                    for k in filter_data:
                        print("137")
                        if k['time'][:10] == curdatetime[:10] and k['count'] >= int(user_profile['number_of_execution']):
                                return False, f"Thank you for using {api_url}! Our standard API rate limit is  {user_profile['number_of_execution']} requests per day."
                                # return Response({'status': status.HTTP_200_OK, 'message': f"Thank you for using {api_url}! Our standard API rate limit is  {user_profile['number_of_execution']} requests per day."})                    
                            # return Response({'status': status.HTTP_200_OK, 'message': f"Thank you for using {api_url}! Our standard API rate limit is  {user_profile['number_of_execution']} requests per day."})
                    DataList = [{
                        "user_id": api_key_detail.user_id,
                        "api_url": api_url,
                        "time": curdatetime,
                        "status": "running",
                        "count": 1
                    }]
                    UserAPILogJsonFile(fileName, DataList)
                    return True, "Sucess"
                            
                else:
                    DataList = [{
                        "user_id": api_key_detail.user_id,
                        "api_url": api_url,
                        "time": curdatetime,
                        "status": "running",
                        "count": 1
                    }]
                    UserAPILogJsonFile(fileName, DataList)

                    return True, "Success" 

            return False, "Authentication Fails Or Api Not Found"  
        else:
            return False, "Authentication Fails"
   except Exception as err:
       return False, f"Something error or Authentication Fails or {err}"




def UserMetaProfileCheck(user_id, datasource):
    try:
        user_meta_profile_data = Table_data_info.objects.filter(table_id=632, table_col_id=4,  column_data=datasource,  column_name='datasource', user_id=user_id)[0]
        user_meta_profile_data_detail = Table_data_info.objects.filter(table_id=632, table_ref_id=user_meta_profile_data.table_ref_id, user_id=user_meta_profile_data.user_id)

        user_meta_profile = {}
        column_name=[]
        column_active=[]
        # print("user_meta_profile_data_detail", len(user_meta_profile_data_detail))
        if user_meta_profile_data_detail:
            for m in user_meta_profile_data_detail:
                user_meta_profile['user_id'] = m.user_id
                # user_meta_profile[m.column_name] = m.column_data
                if m.column_name == 'meta_data_profile_id':
                    # key_name = Table_data_info.objects.get(table_data_id=m.column_data)
                    key_name_data = Table_data_info.objects.get(table_data_id=int(m.column_data))
                    # print("key_name_data", key_name_data.column_data)
                    column_name.append(key_name_data.column_data)
                    s_data = Table_data_info.objects.filter(table_id=631, table_col_id=1, table_ref_id=key_name_data.table_ref_id, user_id=key_name_data.user_id)[0]
                    user_meta_profile['datasource_type'] = s_data.column_data
                if m.column_name == 'active':
                    column_active.append(m.column_data)

                if m.column_name == 'datasource':
                    user_meta_profile[m.column_name] = m.column_data

        user_meta_profile['column_name'] = column_name
        user_meta_profile['column_active'] = column_active
        # print("215 user_meta_profile", user_meta_profile)
        record_data = ""
        record_data_detail = ""
        try:
            record_data = Table_data_info.objects.filter(table_id=633, table_col_id=5,  column_data=datasource,  column_name='datasource', user_id=user_id)[0]
            record_data_detail = Table_data_info.objects.filter(table_id=633, table_ref_id=record_data.table_ref_id, user_id=record_data.user_id)
        except:
            pass

        row_name = []
        row_data_section = {}
        if len(record_data_detail) !=0:
            for k in record_data_detail:
                if k.column_name == 'meta_data_profile_id':
                    key_name_data = Table_data_info.objects.get(table_data_id=int(k.column_data))
                    row_data_section['column_name']=key_name_data.column_data

                if k.column_name == 'operator':
                    row_data_section[k.column_name]=k.column_data

                if k.column_name == 'rec_value':
                    row_data_section[k.column_name]=k.column_data

                if len(row_data_section) == 3:
                    row_name.append(row_data_section)
                    row_data_section={}

        user_meta_profile['row_name'] = row_name

        # print("column_name", column_name)  
        # print("column_active", column_active)  
        # print("user_meta_profile", user_meta_profile) 

        # fileName = main_media_url+f"/media/upload_file/yahoo_finance_hist/{user_meta_profile['datasource']}"
        # DataListItem=[]
        # SectionDict={}
        # if os.path.isfile(fileName):
        #     f = open(fileName)
        #     data = json.load(f)
        #     array_data_list = data['data']
        #     # print("array_data_list", array_data_list)
            
        #     for kd in array_data_list:
        #         # print("kd", kd)
        #         if len(user_meta_profile['column_name']) == len(user_meta_profile['column_active']):
        #             for i in range(len(user_meta_profile['column_name'])):
        #                 # if user_meta_profile['column_active'][i] == 'True':
        #                 #     key_name = user_meta_profile['column_name'][i]
        #                 #     # print("key_name", key_name)
        #                 #     # print("i", i, user_meta_profile['column_name'][i], kd[user_meta_profile['column_name'][i]])
        #                 #     SectionDict[key_name]=kd[key_name]
        #                 if user_meta_profile['column_active'][i] == 'False':  
        #                     # print("i", i, user_meta_profile['column_active'][i])
        #                     key_name = user_meta_profile['column_name'][i] 
        #                     SectionDict[key_name]="restricted"
        #                 else:  
        #                    key_name = user_meta_profile['column_name'][i]
        #                    SectionDict[key_name]=kd[key_name]
        #         # print("SectionDict", SectionDict, len(SectionDict))        
        #         if len(SectionDict) != 0:
        #             DataListItem.append(SectionDict)
        #             SectionDict={}
        # print("DataListItem", DataListItem)

        return True, "success", user_meta_profile  
    except Exception as err:
       return False, f"Something error or UserMetaProfileCheck  or {err}", []


def UserMetaProfileRestrictedDataCheck(real_data_list, column_name_list, column_active_list, row_name_list, user_id, datasource):
    curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
    try:
        DataListItem=[]
        DataListItem1=[]
        SectionDict={}

        for kd in real_data_list:
            # print("kd", kd)
            if len(column_name_list) == len(column_active_list):
                for i in range(len(column_name_list)):
                    if column_active_list[i] == 'False':  
                        # print("i", i, user_meta_profile['column_active'][i])
                        key_name = column_name_list[i] 
                        SectionDict[key_name]="restricted"
                    else:  
                        key_name = column_name_list[i]
                        SectionDict[key_name]=kd[key_name]
            # print("SectionDict", SectionDict, len(SectionDict)) 
            if len(SectionDict) != 0:
                DataListItem.append(SectionDict)
                SectionDict={}

        if len(row_name_list) != 0:
            for d in DataListItem:
                count=0
                for j in row_name_list:
                    count+=1
                    if j['operator'] == '>':
                        # print("j", j) 
                        key = j['column_name']
                        if d[key] > int(j['rec_value']):
                            pass 
                        else:
                            d={}      

                    if j['operator'] == '<':
                        # print("j", j) 
                        key = j['column_name']
                        if d[key] < int(j['rec_value']):
                           pass
                        else:
                            d={}   
                        # else:
                        #     SectionDict[key] = 'restricted' 

                    if j['operator'] == '>=':
                        # print("j", j)  
                        key = j['column_name']
                        if d[key] >= int(j['rec_value']):
                           pass
                        else:
                            d={}   
                if count == len(row_name_list) and len(d) !=0:
                    DataListItem1.append(d)
        else:
            DataListItem1=DataListItem
            
            
        # print("DataListItem", DataListItem)
        GeneralLogFunction(Process_Name=f"{user_id} {datasource} data fetch",  Time=curdatetime, error="success")
        return True, "success", DataListItem1  
    except Exception as err:
        GeneralLogFunction(Process_Name=f"{user_id} {datasource} data fetch",  Time=curdatetime, error=f"Something error or UserMetaProfileRestrictedDataCheck  or {err}")
        return False, f"Something error or UserMetaProfileRestrictedDataCheck  or {err}", []

# xlsx data
def userMetaDataXlSX(fileName, datasource, user_id):
    try:

        main_df = pd.read_excel(fileName)
        real_data_list = JsonConvertData(main_df)
        result, message, main_data = UserMetaProfileCheck(user_id, datasource) 
        column_name_list = main_data['column_name']
        column_active_list = main_data['column_active']
        row_name_list = main_data['row_name']

        result1, message1, main_data1 = UserMetaProfileRestrictedDataCheck(real_data_list, column_name_list, column_active_list, row_name_list, user_id, datasource)
        return result1, message1, main_data1
    except Exception as err:
       return False, f"Something error or userMetaData  or {err}", []


# json data
def userMetaDataJson(fileName, datasource, user_id):
    try:
        real_data_list = ""
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            real_data_list = data['data']

        result, message, main_data = UserMetaProfileCheck(user_id, datasource) 
        column_name_list = main_data['column_name']
        column_active_list = main_data['column_active']
        row_name_list = main_data['row_name']

        result1, message1, main_data1 = UserMetaProfileRestrictedDataCheck(real_data_list, column_name_list, column_active_list, row_name_list, user_id, datasource)
        return result1, message1, main_data1
    except Exception as err:
       return False, f"Something error or userMetaData  or {err}", []    

# model data
def userMetaDataModel(data, datasource, user_id):
    try:

        real_data_list = data
        result, message, main_data = UserMetaProfileCheck(user_id, datasource) 
        print("main_data", main_data)
        column_name_list = main_data['column_name']
        column_active_list = main_data['column_active']
        row_name_list = main_data['row_name']

        result1, message1, main_data1 = UserMetaProfileRestrictedDataCheck(real_data_list, column_name_list, column_active_list, row_name_list, user_id, datasource)
        return result1, message1, main_data1
    except Exception as err:
       return False, f"Something error or userMetaData  or {err}", []    

#Sorting List
def Sorting(lst):
    lst.sort(key=len)
    return lst

# Wrapper function Multi file check
def WrapperMultiFileCheck(file_name):
    try:
        print("file_name", file_name)
        main_url_list = []
        fileName1 = main_media_url+'/media/upload_file/investing/json'
        dir_list = os.listdir(fileName1)
        # print("dir_list", dir_list)
        # process_data = [x for x in dir_list if x == file_name]
        file_data = [word for word in dir_list if file_name in word]
        # print("file_data", file_data)
        for f in file_data:
            main_url_list.append(fileName1+"/"+f)
        # print("main_url_list 1", main_url_list)  
        main_url_list = Sorting(main_url_list) 
        # print("main_url_list 2", main_url_list)   
        
        final_data = []
        final_section = {}

        if file_name == "process_log":
            # fileName = main_media_url+f"/media/upload_file/investing/json/process_log.json"
            for fn in main_url_list:
                # print("fn", fn)
                if os.path.isfile(fn):
                    f = open(fn)
                    data = json.load(f)
                    # print("data", data)
                    # array_data_list = data['data']
                    if len(data) !=0:
                        try:
                            for m in data:
                                # print("m", m)
                                # print("data[m]", data[m])
                                for k in data[m]:
                                    # print("k", k)
                                    # print("data[m][k]", data[m][k])
                                    final_section=data[m][k]
                                    final_section['Process_Name']=m
                                    final_section['Process_Id']=k
                                    # print("final_section", final_section)
                                    if len(final_section)!=0:
                                        final_data.append(final_section)
                                        final_section={}
                        except:
                            for m in data:
                                # print("m.split", m.split("-")[0])
                                # dList = [x for x in final_data if x['Process_Id'].split("-")[0] == m.split("-")[0]][0]['Process_Name']
                                # print("dList", dList)
                                final_section=data[m]
                                final_section['Process_Name']=[x for x in final_data if x['Process_Id'].split("-")[0] == m.split("-")[0]][0]['Process_Name']
                                final_section['Process_Id']=m
                                if len(final_section)!=0:
                                    final_data.append(final_section)
                                    final_section={}

        # print("final_data", final_data)  
        return True, "Success",  final_data                         
    except Exception as err:
       return False, f"Something error or userMetaData  or {err}", []  