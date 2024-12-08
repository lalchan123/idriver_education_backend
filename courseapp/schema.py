import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter, CharFilter
import json
import csv
from rest_framework_simplejwt.tokens import RefreshToken
from graphql import GraphQLError

import requests

import time
# import datetime
from datetime import datetime

from pandas import *


from courseapp.helpers import *
from courseapp.send_mail import *


from django.db.models import Q

import channels_graphql_ws
import channels
import graphql_jwt


from courseapp.models import *

from accountapp.DynamicFunction.ValidatorFG import *
from media.upload_file.dynamic_rest.GQGetAPI import *

# global function
from FunctionFolder.WrapperFunc import *

from accountapp.Decorators import *



gm = time.strftime("%a, %d %b %Y %X",time.gmtime())
currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%d/%m/%Y')
currenttimedateE = datetime.fromtimestamp(currenttimestamp).strftime('%d-%m-%Y')


# global function
from FunctionFolder.WrapperFunc import *




class CourseInfoType(DjangoObjectType):
    class Meta:
        model = course_info
        fields = '__all__'
        
class ContentDescriptionMasterType(DjangoObjectType):
    class Meta:
        model = ccon_desc_master
        fields = '__all__'       
        
class ContentDescriptionDetailType(DjangoObjectType):
    class Meta:
        model = ccon_desc_dtl
        fields = '__all__'      
        
class ContentMcqMasterType(DjangoObjectType):
    class Meta:
        model = ccon_mcq_mst
        fields = '__all__'
        
class ContentMcqDetailType(DjangoObjectType):
    class Meta:
        model = ccon_mcq_dtl
        fields = '__all__' 
        
        
class TableDataJsonDynamicInfoType(DjangoObjectType):
    class Meta:
        model = JsonDynamicModel
        fields = '__all__'
        
                         
class TableInfoDtlType(DjangoObjectType):
    class Meta:
        model = Table_info_dtl
        fields = '__all__' 
        
class TableColInfoType(DjangoObjectType):
    class Meta:
        model = Table_col_info
        fields = '__all__' 
                          
class TableDataInfoType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__'  
        
class TableDataMdInfoType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__' 
        
class TableDataJsonInfoType(DjangoObjectType):
    class Meta:
        model = JsonModel
        fields = '__all__'      
        

class GETTableDataInfoType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__'         
        
    item_data = graphene.String()  
    data1 = graphene.JSONString()
    
class GETMCQTableDataInfoType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__'         
        
    mcq_data = graphene.String()  
    
    
class GETJSONFILEType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__'
    json_data = graphene.String()
    success_message = graphene.String()  
    error_message = graphene.String()
    
class GETValidateType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        fields = '__all__'
    validate = graphene.Boolean()    
    
class TableDataRelayNodeInfoType(DjangoObjectType):
    class Meta:
        model = Table_data_info
        filter_fields = ['user_id', 'table_data_id', 'table_ref_id', 'table_id', 'table_col_id', 'column_data', 'column_name']
        interfaces = (graphene.relay.Node, ) 
        
class TableDataRelayNodeInfoTypeFilter(FilterSet):
    class Meta:
        model = Table_data_info
        fields = '__all__'

        
    order_by = OrderingFilter(
               fields=(
                ('table_ref_id'),
                )
            )         
        
        
def table_data_md_mid(table_id, col_id, column_data):
    ids = []
    tbdata = Table_data_info.objects.all()
    for tdata in tbdata:
        if tdata.table_id==table_id and tdata.table_col_id==col_id and tdata.column_data==column_data:
            ids.append(str(tdata.table_id) + "." + str(tdata.table_col_id))
    
    print('62', ids)  
    return ids    
    
    
    
def GetTableDataJson():
    # Opening JSON file
    f = open('/home/itbusaah/idrivereducation/courseapp/tabledatainfo.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    json_data = dict() 
    table_key = []
    table_value = []
    
    for json_data in data['data']:
        table_value.append("data")
        for i, k in json_data.items():
            # print(i)
            table_key.append((str(i)+":"+str(k)))
     
    return table_key, table_value  
    
    
    
def JsonLogFile(log_time):
    def write_json(new_data, filename='/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/logfile.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["timelog"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
    y = {
        "log_time": log_time
        }
        
    write_json(y) 
    

def AppJsonLogFile(log_event, log_time):
    def write_json(new_data, filename='/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/applog.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["AppLog"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
    y = {
        "log_event": log_event,
        "log_time": log_time
        }
        
    write_json(y)     
    
    
    

class JsonDataInfoType(graphene.ObjectType):
    column_name = graphene.String()        
    column_data = graphene.String()
    
    
class SignInInfoType(graphene.ObjectType):
    result = graphene.Boolean()  
    
    
class Section(graphene.ObjectType):
    key = graphene.String()        # dictionary key
    header = graphene.String()     # dictionary value    
    
    
    
class FileNameInput(graphene.InputObjectType):
    file_name = graphene.String()


# def MergeArrayJson(filename):
#     DataList = []
#     DataDict = {}
#     for f1 in filename:
#         fname = f1['file_name']
#         with open(f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/yahoo_finance_hist/{fname}.json', 'r') as file:
#             fileData = json.load(file)
#             DataDict[fname]=fileData["data"]
#             if DataDict != "":
#                 DataList.append(DataDict)
#                 DataDict={}    
#     return DataList    
        


        
                
        
class Query(graphene.ObjectType):
    
    get_table_info_dtl = graphene.Field(TableInfoDtlType, table_name = graphene.String(required=True))
    get_table_col_info = graphene.List(TableColInfoType, table_id = graphene.Int(required=True))
    
    all_contacts = DjangoFilterConnectionField(TableDataRelayNodeInfoType, filterset_class=TableDataRelayNodeInfoTypeFilter)
    table_data_md = graphene.List(TableDataMdInfoType, table_id=graphene.Int(), col_id=graphene.Int(), column_data=graphene.String())
    get_table_data_info = graphene.List(TableDataInfoType, table_id=graphene.Int(), col_id=graphene.Int(), column_data=graphene.String())
    # get_table_data_rel_id_info = graphene.List(TableDataInfoType, table_id=graphene.Int(), table_col_id=graphene.Int(), tab_rel_id=graphene.String(), api_key=graphene.String(required=True))
    get_table_data_rel_id_info = graphene.List(TableDataInfoType, table_id=graphene.Int(), table_col_id=graphene.Int(), tab_rel_id=graphene.String())
    get_table_data_ref_id_info = graphene.List(TableDataInfoType, table_id=graphene.Int(), table_col_id=graphene.Int(), table_ref_id=graphene.String())
    get_table_data_ref_id_info_update = graphene.List(TableDataInfoType, table_id=graphene.Int(), table_col_id=graphene.Int(), table_ref_id=graphene.Int())
    
    get_table_data_json_info = graphene.Field(JsonDataInfoType)
    
    
    user_sign_in = graphene.Field(SignInInfoType, email=graphene.String(required=True), password=graphene.String(required=True))
    
    table_json_data_model= graphene.List(Section, table_id=graphene.Int())
    
    q_get_table_data_info = graphene.Field(GETTableDataInfoType, Qselect=graphene.String(required=True), Qfrom=graphene.String(required=True), Qwhere=graphene.String(required=False))
    q_get_table_data_info1 = graphene.Field(GETTableDataInfoType, Qselect=graphene.String(required=True), Qfrom=graphene.String(required=True), Qwhere=graphene.String(required=False))
    q_get_multi_table_data_info = graphene.Field(GETTableDataInfoType, Qselect=graphene.String(required=True), QTable1=graphene.String(required=True), QTable2=graphene.String(required=True), Qwhere=graphene.String(required=False))
    
    
    get_course_info_dynamic = graphene.List(TableDataInfoType)
    get_course_content_desc_master_dynamic = graphene.List(TableDataInfoType)
    get_course_content_desc_detail_dynamic = graphene.List(TableDataInfoType)
    get_course_content_mcq_master_dynamic = graphene.List(TableDataInfoType)
    get_course_content_mcq_detail_dynamic = graphene.List(TableDataInfoType)



    course_info = graphene.List(CourseInfoType)
    content_description_master = graphene.List(ContentDescriptionMasterType)
    content_description_detail = graphene.List(ContentDescriptionDetailType)
    content_mcq_master = graphene.List(ContentMcqMasterType)
    content_mcq_detail = graphene.List(ContentMcqDetailType)
    
        
    table_info_dtl = graphene.List(TableInfoDtlType)
    table_col_info = graphene.List(TableColInfoType)
    table_data_info = graphene.List(TableDataInfoType)    
    user_table_data_info = graphene.List(TableDataInfoType, table_id= graphene.Int(required=True), tab_rel_id= graphene.String())    
    userdetails_table_data_info = graphene.List(TableDataInfoType) 
    
    get_first_slider_home = graphene.List(TableDataInfoType)
    get_second_slider_home = graphene.List(TableDataInfoType)
    get_third_slider_home = graphene.List(TableDataInfoType)
    get_fourth_slider_home = graphene.List(TableDataInfoType) 
    
    get_event_invitation = graphene.List(TableDataInfoType)
    get_all_event_invitation = graphene.List(TableDataInfoType, event_user_id = graphene.String(required=True))
    get_unique_event_invitation = graphene.List(TableDataInfoType, table_id = graphene.Int(required=True), table_ref_id = graphene.Int(required=True))
    get_event_contact = graphene.List(TableDataInfoType, event_contact_user_id = graphene.String(required=True), event_title = graphene.String(required=True), bbt = graphene.String(required=True))
    get_event_contact1 = graphene.List(TableDataInfoType, event_contact_user_id = graphene.String(required=True))
    get_all_user_contact = graphene.List(TableDataInfoType, event_user_id = graphene.String(required=True))
    get_all_user_contact2 = graphene.List(TableDataInfoType, event_user_id = graphene.String(required=True))
    get_all_user_contact3 = graphene.List(TableDataInfoType, event_user_id = graphene.String(required=True))
    get_all_user_contact_ref = graphene.Field(GETTableDataInfoType, event_user_id = graphene.String(required=True))
    get_all_user_contact_paginate = graphene.List(TableDataInfoType, event_user_id = graphene.String(required=True), first=graphene.Int(), skip=graphene.Int())
    
    
    get_mcq = graphene.Field(GETMCQTableDataInfoType, tab_rel_id = graphene.String(required=True))
    get_course_to_mcq = graphene.Field(GETMCQTableDataInfoType,  course_id = graphene.String(required=True))
    get_question_bank = graphene.Field(GETMCQTableDataInfoType, course_id = graphene.String(required=True))
    get_chapter_check = graphene.Field(GETMCQTableDataInfoType, course_id = graphene.String(required=True), user_id = graphene.String(required=True))
    get_chapter = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True), tab_rel_id = graphene.String(required=True))
    get_chapter_content_dtl = graphene.Field(GETMCQTableDataInfoType, tab_rel_id = graphene.String(required=True))
    get_course = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True))
    get_dummy_user_course = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True))
    get_course_complete_certificate = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True), course_id = graphene.String(required=True))
    get_course_progresbar = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True), course_id = graphene.String(required=True))
    get_exam_course_mcq_final_result = graphene.Field(GETMCQTableDataInfoType, user_id = graphene.String(required=True), course_id = graphene.String(required=True))
    
    
    get_excel_file = graphene.Field(GETMCQTableDataInfoType)
    get_yahoo_csv_file = graphene.Field(GETMCQTableDataInfoType)
    get_all_latest_news_json = graphene.Field(GETMCQTableDataInfoType)
    
    
    get_column_dtl = graphene.Field(GETMCQTableDataInfoType, table_id = graphene.String(required=True))
    
    get_app_menu = graphene.Field(GETMCQTableDataInfoType)
    get_faq_help = graphene.Field(GETMCQTableDataInfoType)
    
    get_search_query = graphene.Field(GETMCQTableDataInfoType, search=graphene.String())
    get_course_related_search = graphene.Field(GETMCQTableDataInfoType, search=graphene.String())
    
    get_cnbc_news = graphene.Field(GETMCQTableDataInfoType)
    
    get_node_design = graphene.Field(GETMCQTableDataInfoType, name=graphene.String())
    
    get_node_design_data = graphene.Field(GETMCQTableDataInfoType, name=graphene.String())
    
    
    get_yahoo_info_file_name = graphene.Field(GETJSONFILEType)
    get_yahoo_hist_file_name = graphene.Field(GETJSONFILEType)
    
    
    get_json_data_merge = graphene.Field(GETJSONFILEType, api_key=graphene.String(), codeFile=graphene.String(), fileList=graphene.List(FileNameInput))
    
    get_dynamic_table_field = graphene.Field(GETJSONFILEType, table_id=graphene.Int())
    get_dynamic_table_field_user = graphene.Field(GETJSONFILEType, table_id=graphene.Int(), user_id=graphene.String())
    get_all_table_column = graphene.Field(GETJSONFILEType)
    
    
    get_dynamic_table_json_field = graphene.List(TableDataJsonDynamicInfoType, table_id=graphene.Int())



    get_rule_validate_frontend = graphene.Field(GETValidateType, table_name=graphene.String(), column_name=graphene.String(), operator=graphene.String(), value=graphene.String())
    get_value_validate_frontend = graphene.Field(GETValidateType, table_name=graphene.String(), column_name=graphene.String(), column_value=graphene.String(), operator=graphene.String(), value=graphene.String())

    get_dynamic_gq_api = graphene.Field(GETJSONFILEType, api_name=graphene.String(), user=graphene.String())
    
    
    
    def resolve_get_dynamic_gq_api(self, info, api_name, user):
        try:
            startTime = CurrentTimeFunc()
            
            APICALLFUNCTION('get_dynamic_gq_api', 'null')
            
            # Data = []
       
            # TableDataRef = []
            # Data = []
            # func_name = ""
            # username = ""
            # api_name_value = Table_data_info.objects.filter(table_id=579, table_col_id=1, column_data=api_name)
            # if len(api_name_value) != 0:
            #     for m in api_name_value:
            #       TableDataRef += Table_data_info.objects.filter(table_id=579, table_ref_id=m.table_ref_id)

            # for k in TableDataRef:
            #     if k.table_id == 579 and k.table_col_id==3:
            #         if k.column_data == "GQGetAPI":
            #             func_name = k.column_data

            #     if k.table_id == 579 and k.table_col_id==4:
            #         if k.column_data == user:
            #             username = k.column_data   
                          

            #     if k.table_id == 579 and k.table_col_id==7:
            #         if k.column_name == "api_parameter" and func_name == "GQGetAPI" and username == user:
            #             Data = GQGetAPI(user, api_name, json.loads(k.column_data))
            
            
            sections = {}
            items = []
            refId = []
            api_name_value = Table_data_info.objects.filter(table_id=579)
            for k in api_name_value:
                refId.append(k.table_ref_id)
                        
            refId = list(set(refId))

            for m in refId:
                for i in api_name_value:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}

            item_data = [x for x in items if x['api_name'] == api_name and x['user'] == user] 
            

        
            fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/pipelineapicreatecode.json'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['data']

                for id in item_data:
                    item_arr_data = [x for x in array_data if x['api_name'] == id['api_name'] and x['user'] == id['user'] and x['api_url'] == id['api_url'] and x['api_method'] == id['api_file'] and x['api_data_fetch_type'] == id['api_data_fetch_type']] 
                    for m in item_arr_data:
                        loc = {}
                        exec(m['code'],  globals(), loc)            
               
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(loc['result'])
            DataFetch_Static("get_dynamic_gq_api", "get_dynamic_gq_api function", value_count, round(loadTime, 6))
            
            return GETJSONFILEType(json_data=loc['result'])
        except Exception as err:
            return Exception(f"Somethings error or {err}")    

    
    
    def resolve_get_rule_validate_frontend(self, info, table_name, column_name, operator, value):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_rule_validate_frontend', 'null')
            
            if operator == 'is not NULL' or operator == 'is not null':
                result = IsNotNullFunctionRuleValidate(table_name, column_name, operator, value)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(result)
                DataFetch_Static("get_rule_validate_frontend", "IsNotNullFunctionRuleValidate function", value_count, round(loadTime, 6))
                return GETValidateType(validate=result)

            if operator == 'is unique' or operator == 'is UNIQUE':
                result = IsUniqueFunctionRuleValidate(table_name, column_name, operator, value)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(result)
                DataFetch_Static("get_rule_validate_frontend", "IsNotNullFunctionRuleValidate function", value_count, round(loadTime, 6))
                return GETValidateType(validate=result)
            else:
                return Exception("operator is not found please valid operator")
            
        except Exception as err:
            return Exception(f"Somethings error or {err}")
         
        
    def resolve_get_value_validate_frontend(self, info, table_name, column_name, column_value, operator, value):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_value_validate_frontend', 'null')
            if operator == 'is not NULL' or operator == 'is not null':
                result = IsNotNullFunctionValueValidate(table_name, column_name, column_value, operator, value)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(result)
                DataFetch_Static("get_value_validate_frontend", "IsNotNullFunctionValueValidate function", value_count, round(loadTime, 6))
                return GETValidateType(validate=result)

            if operator == 'is unique' or operator == 'is UNIQUE':
                result = IsUniqueFunctionValueValidate(table_name, column_name, column_value, operator, value)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(result)
                DataFetch_Static("get_value_validate_frontend", "IsUniqueFunctionValueValidate function", value_count, round(loadTime, 6))
                return GETValidateType(validate=result)
            
            if operator == 'contains' or operator == 'CONTAINS':
                result = ContainsFunctionValueValidate(table_name, column_name, column_value, operator, value)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(result)
                DataFetch_Static("get_value_validate_frontend", "ContainsFunctionValueValidate function", value_count, round(loadTime, 6))
                return GETValidateType(validate=result)
            else:
                return Exception("operator is not found please valid operator")
            
        except Exception as err:
            return Exception(f"Somethings error or {err}") 
    
    def resolve_q_get_table_data_info(self, info, Qselect, Qfrom, Qwhere):
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('q_get_table_data_info', 'null')
        sections={}
        items = []
        refId = []
        if Qselect=="*" and Qfrom!="" and Qwhere == "": 
            qTableid = Table_info_dtl.objects.get(table_name=Qfrom)
            dTableData = Table_data_info.objects.filter(table_id=qTableid.table_id)
            for k in dTableData:
                refId.append(k.table_ref_id)
            refId = list(set(refId))
            
            for m in refId:
                for i in dTableData:
                    if i.table_ref_id==m:
                        sections[i.column_name]  = i.column_data
                        
                
                if sections != "":
                    items.append(sections)
                    sections={}
            

            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("q_get_table_data_info", "model data", value_count, round(loadTime, 6))
            
            return GETTableDataInfoType(item_data=items)
            
            
    def resolve_q_get_multi_table_data_info(self, info, Qselect, QTable1, QTable2, Qwhere):
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('q_get_multi_table_data_info', 'null')
        sections={}
        items = []
        refId = []
        if Qselect=="*" and QTable1!="" and QTable2 !="" and Qwhere == "": 
            qTableid1 = Table_info_dtl.objects.get(table_name=QTable1)

            qTableid2 = Table_info_dtl.objects.get(table_name=QTable2)
            
            dTableData = Table_data_info.objects.filter(table_id=qTableid2.table_id, tab_rel_id=qTableid1.table_id)


            for k in dTableData:
                refId.append(k.table_ref_id)

            refId = list(set(refId))
            
            for m in refId:
                for i in dTableData:
                    if i.table_ref_id==m:
                        sections[i.column_name]  = i.column_data
                        
                
                if sections != "":
                    items.append(sections)
                    sections={}
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("q_get_multi_table_data_info", "model data", value_count, round(loadTime, 6))        

            return GETTableDataInfoType(item_data=items)
            
            
            
    def resolve_q_get_table_data_info1(self, info, Qselect, Qfrom, Qwhere):
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('q_get_table_data_info1', 'null')
        jsonStringData={}
        sections={}
        items = []
        if Qselect=="*" and Qfrom!="" and Qwhere == "": 
            qTableid = Table_info_dtl.objects.get(table_name=Qfrom)
            print("247", qTableid.table_id)
            # return qTableid
            dTableData = Table_data_info.objects.filter(table_id=qTableid.table_id)
            print("250", dTableData)
            for i in dTableData:
                if i.table_col_id==1:
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==2:
                    sections[i.column_name]  = i.column_data
                    items.append(sections)
                    sections={}
            
            
            print("263", items)
            jsonStringData['data'] = items
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("q_get_table_data_info1", "model data", value_count, round(loadTime, 6)) 
            
            return GETTableDataInfoType(data1=jsonStringData)
    
    
    def resolve_table_json_data_model(self, info, table_id):
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('table_json_data_model', 'null')
        # sections = {
        #   's1': "Section 1",
        #   's2': "Section 2",
        #   's3': "Section 3",
        #   's4': "Section 4"
        # }
        sections={
           
        }
        A={}
        B={}
        C={}
        
        data = Table_data_info.objects.filter(table_id=table_id)
        
        for i in data:
            # print("223", i)
            # print("223", i.table_col_id)
            # print("224", i.column_data)
            # print("225", i.table_data_id)
            # print("226", i.tab_rel_id)
            
            if i.tab_rel_id is not None:  #all data 
                parentRecord = Table_data_info.objects.filter(table_data_id=i.tab_rel_id, tab_rel_id=None)  #first parent 
 
                for pdata in parentRecord:
                    print('233', pdata.table_col_id)
                    print('234', pdata.tab_rel_id)
                    sections[pdata.table_col_id]=pdata.column_data
                    
                    childRecord = Table_data_info.objects.filter(tab_rel_id=pdata.table_data_id)
                    for cdata in childRecord:
                        # print("248", cdata.column_data)
                        B[str(cdata.table_col_id)+" "+str(cdata.table_data_id)]=cdata.column_data
                        # try to check whether it has any child 
                        childRecord_parent = Table_data_info.objects.filter(tab_rel_id=cdata.table_data_id) #second parent 
                        for cdata_p  in  childRecord_parent:
                            print("256", cdata_p)
                            C[str(cdata_p.table_col_id)+" "+str(cdata_p.table_data_id)]=cdata_p.column_data

                            sections[cdata_p.tab_rel_id] = C
                            sections[pdata.table_data_id] = B
                
            else:
                sections[i.table_col_id]=i.column_data
                    
                
            
            
            # if i.table_col_id<=5:
            #     sections['A'][i.table_col_id]=i.column_data
            #     if i.table_col_id<=2:
            #         sections['A']['C'][i.table_col_id]=i.column_data
            # else:
            #     sections['B'][i.table_col_id]=i.column_data
            
        sections_as_obj_list = [] # Used to return a list of Section types

        # Create a new Section object for each item and append it to list
        for key, value in sections.items(): # Use sections.iteritems() in Python2
            section = Section(key, value) # Creates a section object where key=key and header=value
            sections_as_obj_list.append(section)
            
        endTime = CurrentTimeFunc()
        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(sections_as_obj_list)
        DataFetch_Static("table_json_data_model", "model data", value_count, round(loadTime, 6))     

        # return sections
        return sections_as_obj_list  
        
        
    def resolve_get_dynamic_table_field(self, info, table_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_dynamic_table_field', 'null')
            sections = {}
            items = []
            refId = []
            table_data = Table_data_info.objects.filter(table_id=table_id).order_by('-table_ref_id')
            for k in table_data:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))

            for m in refId:
                for i in table_data:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_id']=i.table_id
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}     


            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_dynamic_table_field", "model data", value_count, round(loadTime, 6))   
            
            return GETJSONFILEType(json_data=items) 
        except Table_data_info.DoesNotExist:
            return None  
    
    
    
    def resolve_get_dynamic_table_json_field(self, info, table_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_dynamic_table_json_field', 'null')
            
            datajson = JsonDynamicModel.objects.filter(table_id=table_id)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(datajson)
            DataFetch_Static("get_dynamic_table_json_field", "model json data", value_count, round(loadTime, 6))  
            
            return datajson
        except JsonDynamicModel.DoesNotExist:
            return None
            
    def resolve_get_dynamic_table_field_user(self, info, table_id, user_id):
        try:
            startTime = CurrentTimeFunc()
            
            APICALLFUNCTION('get_dynamic_table_field_user', 'null')
            
            sections = {}
            items = []
            refId = []
            table_data = Table_data_info.objects.filter(table_id=table_id, user_id=user_id).order_by('-table_ref_id')
            for k in table_data:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))

            for m in refId:
                for i in table_data:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_id']=i.table_id
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}  
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_dynamic_table_field_user", "model data", value_count, round(loadTime, 6))        

            return GETJSONFILEType(json_data=items) 
        except Table_data_info.DoesNotExist:
            return None        
    
    
    def resolve_get_all_table_column(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_table_column', 'null')
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}
            table_info = Table_info_dtl.objects.all().order_by('-table_id')
            for t in table_info:
                tableSections['table']=t.table_name
                tableSections['id']=t.table_id

                table_col_info = Table_col_info.objects.filter(table_id=t.table_id)
                for c in table_col_info:
                    columnSections['no']=c.table_col_id
                    columnSections['name']=c.column_name
                    if len(columnSections)!=0:
                        columnItem.append(columnSections)
                        columnSections={}
                tableSections['column']=columnItem       
                if len(tableSections)!=0:
                    tableItem.append(tableSections)
                    tableSections={}
                    columnItem=[]

            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(tableItem)
            DataFetch_Static("get_all_table_column", "model data", value_count, round(loadTime, 6)) 
            
            return GETJSONFILEType(json_data=tableItem) 
        except Table_data_info.DoesNotExist:
            return None
    
        
    def resolve_get_course_info_dynamic(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_info_dynamic', 'null')
            
            data = Table_data_info.objects.filter(table_id=13)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_course_info_dynamic", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None  
            
    def resolve_get_course_content_desc_master_dynamic(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_content_desc_master_dynamic', 'null')
            
            data = Table_data_info.objects.filter(table_id=14, table_col_id=7)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_course_content_desc_master_dynamic", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None  
            
            
    def resolve_get_course_content_desc_detail_dynamic(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_content_desc_detail_dynamic', 'null')
            
            data = Table_data_info.objects.filter(table_id=15, table_ref_id=1)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_course_content_desc_master_dynamic", "model data", value_count, round(loadTime, 6))
            
            return data
        except Table_data_info.DoesNotExist:
            return None   
            
            
    def resolve_get_course_content_mcq_master_dynamic(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_content_mcq_master_dynamic', 'null')
            
            data = Table_data_info.objects.filter(table_id=16, table_col_id=2, table_ref_id=1)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_course_content_desc_master_dynamic", "model data", value_count, round(loadTime, 6))
            
            return data
        except Table_data_info.DoesNotExist:
            return None
        
    def resolve_get_course_content_mcq_detail_dynamic(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_content_mcq_detail_dynamic', 'null')
            
            data = Table_data_info.objects.filter(table_id=17, table_col_id=2, table_ref_id=1, tab_rel_id=5149)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_course_content_mcq_detail_dynamic", "model data", value_count, round(loadTime, 6))
            
            return data
        except Table_data_info.DoesNotExist:
            return None              
    
    def resolve_get_table_info_dtl(self, info, table_name):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_info_dtl', 'null')
            
            data = Table_info_dtl.objects.get(table_name=table_name)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_info_dtl", "model data", value_count, round(loadTime, 6))
            
            return data
        except Table_info_dtl.DoesNotExist:
            return None
        
    def resolve_get_table_col_info(self, info, table_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_info_dtl', 'null')
            
            data = Table_col_info.objects.filter(table_id=table_id)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_info_dtl", "model data", value_count, round(loadTime, 6))
            
            return data
        except Table_col_info.DoesNotExist:
            return None
             
    
    def resolve_table_data_md(self, info, table_id, col_id, column_data ):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('table_data_md', 'null')
            r_id = table_data_md_mid(table_id, col_id, column_data)
            print('126', r_id)
            data_t = Table_data_info.objects.filter(tab_rel_id=r_id[0])
            print('128', data_t)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data_t)
            DataFetch_Static("table_data_md", "model data", value_count, round(loadTime, 6))
            return data_t
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_table_data_info(self, info, table_id, col_id, column_data):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_data_info', 'null')
            if column_data=="":
                data = Table_data_info.objects.filter(table_id=table_id, table_col_id=col_id)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_info", "model data", value_count, round(loadTime, 6))
                return data
            	
            data = Table_data_info.objects.filter(table_id=table_id, table_col_id=col_id, column_data=column_data)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_data_info", "model data", value_count, round(loadTime, 6))	
            return data
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_table_data_rel_id_info(self, info, table_id, table_col_id, tab_rel_id):
        try:
            # result, message = UserLogin(api_key, "get_table_data_rel_id_info")
            # print("973 message", result, message)
            # if result == True:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_data_rel_id_info', 'null')
            if table_col_id==0 and tab_rel_id=="":
                data = Table_data_info.objects.filter(table_id=table_id)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))	
                return data
            elif tab_rel_id=="":
                data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                return data
            elif table_col_id==0:
                data = Table_data_info.objects.filter(table_id=table_id, tab_rel_id=tab_rel_id)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                return data
                    
            data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))    
            return data
            # else:
            #     # return TableDataInfoType(message=message)
            #     raise GraphQLError(message)    
        except Table_data_info.DoesNotExist:
            #  raise GraphQLError("Something error")  
            return None
    
    def resolve_get_table_data_json_info(self, info):
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('get_table_data_json_info', 'null')
        column_name, column_data = GetTableDataJson()
        data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id)
        endTime = CurrentTimeFunc()
        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(column_data)
        DataFetch_Static("get_table_data_json_info", "model data", value_count, round(loadTime, 6))
        return JsonDataInfoType(column_name, column_data)
        
        
    def resolve_user_sign_in(self, info, email, password):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('user_sign_in', 'null')
            
            email_detail = Table_data_info.objects.get(column_data=email)
            password_detail = Table_data_info.objects.get(table_ref_id=email_detail.table_ref_id, column_data=password)
            
            if email_detail.table_ref_id==password_detail.table_ref_id:
                flag_check = Table_data_info.objects.filter(table_ref_id=email_detail.table_ref_id)
             
                email_active = []
                user_active = []
                for i in flag_check:
                    if i.column_name=="is_email_verified" and i.column_data=="True" and i.table_ref_id==email_detail.table_ref_id and i.table_col_id==6:
                        email_active.append(i.column_data)
                    if i.column_name=="is_active" and i.column_data=="True" and i.table_ref_id==email_detail.table_ref_id and i.table_col_id==4:
                        user_active.append(i.column_data)
                
                if email_active and user_active:
                    if email_active[0]=="True" and user_active[0]=="True":
                        endTime = CurrentTimeFunc()
                        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                        value_count = ValueCountFunc(True)
                        DataFetch_Static("user_sign_in", "model data", value_count, round(loadTime, 6))
                        return SignInInfoType(True)
                    else:
                        endTime = CurrentTimeFunc()
                        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                        value_count = ValueCountFunc(False)
                        DataFetch_Static("user_sign_in", "model data", value_count, round(loadTime, 6))
                        return SignInInfoType(False)
                else:
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(False)
                    DataFetch_Static("user_sign_in", "model data", value_count, round(loadTime, 6))    
                    return SignInInfoType(False)
                   
        except Table_data_info.DoesNotExist:
            return None                    
            
    def resolve_course_info(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('course_info', 'null')
            
            data = course_info.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("course_info", "model data", value_count, round(loadTime, 6)) 
            return data
        except course_info.DoesNotExist:
            return None
        
    def resolve_content_description_master(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('content_description_master', 'null')
            data = ccon_desc_master.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("content_description_master", "model data", value_count, round(loadTime, 6)) 
            return data
        except ccon_desc_master.DoesNotExist:
            return None
        
    def resolve_content_description_detail(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('content_description_detail', 'null')
            
            data = ccon_desc_dtl.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("content_description_detail", "model data", value_count, round(loadTime, 6)) 
            return data
        except ccon_desc_dtl.DoesNotExist:
            return None
        
    def resolve_content_mcq_master(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('content_mcq_master', 'null')
            
            data = ccon_mcq_mst.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("content_mcq_master", "model data", value_count, round(loadTime, 6)) 
            return data
        except ccon_mcq_mst.DoesNotExist:
            return None
        
    def resolve_content_mcq_detail(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('content_mcq_detail', 'null')
            data = ccon_mcq_dtl.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("content_mcq_detail", "model data", value_count, round(loadTime, 6))
            return data
        except ccon_mcq_dtl.DoesNotExist:
            return None
        
    def resolve_table_info_dtl(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('table_info_dtl', 'null')
            
            data = Table_info_dtl.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("table_info_dtl", "model data", value_count, round(loadTime, 6))
            return data
        except Table_info_dtl.DoesNotExist:
            return None
        
    def resolve_table_col_info(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('table_col_info', 'null')
            # return Table_col_info.objects.all()
            
            data = Table_col_info.objects.filter(table_id=2)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("table_col_info", "model data", value_count, round(loadTime, 6))
            return data
        except Table_col_info.DoesNotExist:
            return None
            
    def resolve_table_data_info(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('table_data_info', 'null')
            all_data_info = Table_data_info.objects.all()
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(all_data_info)
            DataFetch_Static("table_data_info", "model data", value_count, round(loadTime, 6))
            
            return all_data_info
        except Table_data_info.DoesNotExist:
            return None
    def resolve_user_table_data_info(self, info, table_id, tab_rel_id=None):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('user_table_data_info', 'null')
            if tab_rel_id:
                data = Table_data_info.objects.filter(table_id=table_id).filter(tab_rel_id=tab_rel_id)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("user_table_data_info", "model data", value_count, round(loadTime, 6))
                return data
                
                data = Table_data_info.objects.filter(table_id=table_id).filter(tab_rel_id=tab_rel_id)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("user_table_data_info", "model data", value_count, round(loadTime, 6))    
            return Table_data_info.objects.filter(table_id=table_id)
        except Table_data_info.DoesNotExist:
            return None
    def resolve_get_table_data_ref_id_info(self, info, table_id, table_col_id, table_ref_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_data_ref_id_info', 'null')
            if table_col_id==0 and table_ref_id=="":
                data = Table_data_info.objects.filter(table_id=table_id).order_by('-table_col_id')
            
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_ref_id_info", "model data", value_count, round(loadTime, 6))
                
                return data
                
            data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, table_ref_id=table_ref_id).order_by('-table_col_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_data_ref_id_info", "model data", value_count, round(loadTime, 6))    
            return data
        except Table_data_info.DoesNotExist:
            return None
    def resolve_get_table_data_ref_id_info_update(self, info, table_id, table_col_id, table_ref_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_table_data_ref_id_info_update', 'null')
            if table_id and table_col_id==0 and table_ref_id==0:
                data = Table_data_info.objects.filter(table_id=table_id).order_by('-table_col_id')
            
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_ref_id_info_update", "model data", value_count, round(loadTime, 6))
                
                return data
            if table_id and table_col_id==0 and table_ref_id!=0:
                data = Table_data_info.objects.filter(table_id=table_id, table_ref_id=table_ref_id).order_by('-table_col_id')
            
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_ref_id_info_update", "model data", value_count, round(loadTime, 6))
                return data
            if table_id and table_col_id and table_ref_id==0:
                data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id).order_by('-table_col_id')
            
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_ref_id_info_update", "model data", value_count, round(loadTime, 6))
                return data
                
            data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, table_ref_id=table_ref_id).order_by('-table_col_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_table_data_ref_id_info_update", "model data", value_count, round(loadTime, 6))    
            return data
        except Table_data_info.DoesNotExist:
            return None
                    
    def resolve_userdetails_table_data_info(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('userdetails_table_data_info', 'null')
            userdetail = Table_data_info.objects.filter(table_id=5)

            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(userdetail)
            DataFetch_Static("userdetails_table_data_info", "model data", value_count, round(loadTime, 6))  
            return userdetail
        except Table_data_info.DoesNotExist:
            return None
            
    
    def resolve_get_first_slider_home(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_first_slider_home', 'null')
            data = Table_data_info.objects.filter(table_id=11, table_col_id=1).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_first_slider_home", "model data", value_count, round(loadTime, 6)) 
            return data
        except Table_data_info.DoesNotExist:
            return None
        
    def resolve_get_second_slider_home(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_second_slider_home', 'null')
            data = Table_data_info.objects.filter(table_id=11, table_col_id=2).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_second_slider_home", "model data", value_count, round(loadTime, 6)) 
            return data
        except Table_data_info.DoesNotExist:
            return None
        
    def resolve_get_third_slider_home(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_third_slider_home', 'null')
            data = Table_data_info.objects.filter(table_id=11, table_col_id=3).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_third_slider_home", "model data", value_count, round(loadTime, 6)) 
            return data
        except Table_data_info.DoesNotExist:
            return None
        
    def resolve_get_fourth_slider_home(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_fourth_slider_home', 'null')
            data = Table_data_info.objects.filter(table_id=11, table_col_id=4).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_fourth_slider_home", "model data", value_count, round(loadTime, 6)) 
            return data
        except Table_data_info.DoesNotExist:
            return None  
            
    def resolve_get_event_invitation(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_event_invitation', 'null')
            data = Table_data_info.objects.filter(table_id=4).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_event_invitation", "model data", value_count, round(loadTime, 6)) 
            return data
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_all_event_invitation(self, info, event_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_event_invitation', 'null')
            data = Table_data_info.objects.filter(table_id=4, user_id=event_user_id).order_by('-table_ref_id')
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_all_event_invitation", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None
        
    def resolve_get_unique_event_invitation(self, info, table_id, table_ref_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_unique_event_invitation', 'null')
            data = Table_data_info.objects.filter(table_id=table_id, table_ref_id=table_ref_id)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_unique_event_invitation", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None 
            
    def resolve_get_event_contact(self, info, event_contact_user_id, event_title, bbt):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_event_contact', 'null')
            event_title_details1 = Table_data_info.objects.filter(table_id=4, user_id=event_contact_user_id, column_data=event_title)
            if event_title_details1:
                for k in event_title_details1:
                    if Table_data_info.objects.filter(table_id=4,  user_id=event_contact_user_id, column_data=bbt, table_ref_id=k.table_ref_id).exists():
                        event_title_details = Table_data_info.objects.get(table_id=4, user_id=event_contact_user_id, column_data=event_title, table_ref_id=k.table_ref_id)
                        data = Table_data_info.objects.filter(table_id=5, user_id=event_contact_user_id, tab_rel_id=event_title_details.table_data_id).order_by('-table_ref_id')
                        endTime = CurrentTimeFunc()
                        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                        value_count = ValueCountFunc(data)
                        DataFetch_Static("get_event_contact", "model data", value_count, round(loadTime, 6))
                        return data
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_event_contact1(self, info, event_contact_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_event_contact1', 'null')
            data = Table_data_info.objects.filter(table_id=5).filter(column_data=event_contact_user_id).order_by('-table_ref_id')
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_event_contact1", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None 
            
    def resolve_get_all_user_contact(self, info, event_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_user_contact', 'null')
            data = Table_data_info.objects.filter(table_id=6, user_id=event_user_id).order_by('-table_ref_id')
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_all_user_contact", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None        
    def resolve_get_all_user_contact2(self, info, event_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_user_contact2', 'null')
            data = Table_data_info.objects.filter(table_id=6, user_id=event_user_id)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_all_user_contact2", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None        
    def resolve_get_all_user_contact3(self, info, event_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_user_contact3', 'null')
            data = Table_data_info.objects.filter(table_id=6, user_id=event_user_id)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(data)
            DataFetch_Static("get_all_user_contact3", "model data", value_count, round(loadTime, 6))
            return data
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_all_user_contact_ref(self, info, event_user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_user_contact_ref', 'null')
            sections = {}
            items = []
            refId = []
            contact_user = Table_data_info.objects.filter(table_id=6, user_id=event_user_id).order_by('-table_ref_id')

            for k in contact_user:
                refId.append(k.table_ref_id)
            refId = list(set(refId))
            for m in refId:
                for i in contact_user:
                    if i.table_ref_id==m:
                        sections[i.column_name]  = i.column_data
                        sections["table_id"]  = i.table_id
                        sections["table_ref_id"]  = i.table_ref_id
                        sections["user_id"]  = i.user_id
                        
                
                if sections != "":
                    items.append(sections)
                    sections={}
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_all_user_contact_ref", "model data", value_count, round(loadTime, 6))        
            return GETTableDataInfoType(item_data=items)        
        except Table_data_info.DoesNotExist:
            return None        
            
    def resolve_get_all_user_contact_paginate(self, info, event_user_id, first=None, skip=None, **kwargs):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_user_contact_paginate', 'null')
            qs = Table_data_info.objects.filter(table_id=6, user_id=event_user_id).order_by('-table_ref_id')
            if skip:
                qs = qs[skip:]

            if first:
                qs = qs[:first]

            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(qs)
            DataFetch_Static("get_all_user_contact_paginate", "model data", value_count, round(loadTime, 6))  
            
            return qs    

        except Table_data_info.DoesNotExist:
            return None 
            
            
    def resolve_get_mcq(self, info, tab_rel_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_mcq', 'null')
            sections = {}
            items = []
            refId = []

            sectionsmcqoption = {}
            itemsmcqoption = []
            refIdmcqoption = []

            mcq_question = Table_data_info.objects.filter(table_id=21, tab_rel_id=tab_rel_id).order_by('table_ref_id')

            for k in mcq_question:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))


            for m in refId:
                for i in mcq_question:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            sections[i.column_name]  = i.column_data
                            sections["table_data_id"]  = i.table_data_id
                            mcq_option = Table_data_info.objects.filter(table_id=22, tab_rel_id=i.table_data_id).order_by('table_ref_id')

                            for l in mcq_option:
                                if l.table_col_id==1:
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==2:
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==3:
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==4:
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                    if sectionsmcqoption != "":
                                        itemsmcqoption.append(sectionsmcqoption)
                                        sectionsmcqoption={}                        
                        if i.table_col_id==2:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            sections["options"]  = itemsmcqoption
                if sections != "":
                    items.append(sections)
                    sections={}
                    itemsmcqoption=[]            
            
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_mcq", "model data", value_count, round(loadTime, 6))                            
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None        
    
    
    def resolve_get_course_to_mcq(self, info, course_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_to_mcq', 'null')
            sections = {}
            items = []
            refId = []

            sectionsmcqoption = {}
            itemsmcqoption = []
            chapter_id = []

            course_chapter = Table_data_info.objects.filter(table_id=19, tab_rel_id=course_id).order_by('table_ref_id')
            for ml in course_chapter:
                if ml.table_col_id==1:
                    mcq_question = Table_data_info.objects.filter(table_id=21, tab_rel_id=ml.table_data_id).order_by('table_ref_id')
                    count = 0
                    for i in mcq_question:
                        if i.table_col_id==1:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_data_id"]  = i.table_data_id
                            sections["chapter_id"]  = i.tab_rel_id
                            mcq_option = Table_data_info.objects.filter(table_id=22, tab_rel_id=i.table_data_id).order_by('table_ref_id')
                            countl=0
                            for l in mcq_option:
                                if l.table_col_id==1:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==2:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==3:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==4:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if countl == 4:
                                    if sectionsmcqoption != "":
                                        itemsmcqoption.append(sectionsmcqoption)
                                        sectionsmcqoption={} 
                                        countl = 0                       
                        if i.table_col_id==2:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            sections["options"]  = itemsmcqoption

                        if count == 5:
                            if sections != "":
                                items.append(sections)
                                sections={}
                                itemsmcqoption=[]
                                count = 0
                if ml.table_col_id==2:
                    mcq_question = Table_data_info.objects.filter(table_id=21, tab_rel_id=ml.table_data_id).order_by('table_ref_id')
                    count = 0
                    for i in mcq_question:
                        if i.table_col_id==1:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_data_id"]  = i.table_data_id
                            sections["chapter_id"]  = i.tab_rel_id
                            mcq_option = Table_data_info.objects.filter(table_id=22, tab_rel_id=i.table_data_id).order_by('table_ref_id')
                            countl=0
                            for l in mcq_option:
                                if l.table_col_id==1:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==2:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==3:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if l.table_col_id==4:
                                    countl+=1
                                    sectionsmcqoption[l.column_name]  = l.column_data
                                if countl == 4:
                                    if sectionsmcqoption != "":
                                        itemsmcqoption.append(sectionsmcqoption)
                                        sectionsmcqoption={} 
                                        countl = 0                       
                        if i.table_col_id==2:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            sections["options"]  = itemsmcqoption

                        if count == 5:
                            if sections != "":
                                items.append(sections)
                                sections={}
                                itemsmcqoption=[]
                                count = 0


            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_course_to_mcq", "model data", value_count, round(loadTime, 6))
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
    
    
    def resolve_get_question_bank(self, info, course_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_question_bank', 'null')
            
            sections = {}
            items = []
            refId = []


            mcq_question_bank = Table_data_info.objects.filter(table_id=26, column_data=course_id).order_by('table_ref_id')
            print("1205", mcq_question_bank)

            for k in mcq_question_bank:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))
            print("1216", refId)
            

            for m in refId:
                mcq_question_bank_ref = Table_data_info.objects.filter(table_id=26, table_ref_id=m).order_by('table_ref_id')
                for i in mcq_question_bank_ref:
                    if i.table_ref_id==m:
                        print("1287", i.table_col_id)
                        if i.table_col_id==1:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==2:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            if sections != "":
                                items.append(sections)
                                sections={}
                                
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_question_bank", "model data", value_count, round(loadTime, 6))                    
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None 
            
            
    def resolve_get_app_menu(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_app_menu', 'null')
            
            sections = {}
            items = []
            refId = []


            app_menu = Table_data_info.objects.filter(table_id=33).order_by('table_ref_id')

            for k in app_menu:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))


            for m in refId:
                count = 0
                for i in app_menu:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==2:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            
                        if count == 5:
                            if sections != "":
                                items.append(sections)
                                sections={}
                                count=0
                                
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_app_menu", "model data", value_count, round(loadTime, 6))                      
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_faq_help(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_faq_help', 'null')
            
            sections = {}
            items = []
            refId = []


            faq_help = Table_data_info.objects.filter(table_id=31).order_by('table_ref_id')

            for k in faq_help:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))


            for m in refId:
                count = 0
                for i in faq_help:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==2:
                            count+=1
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            count+=1
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            
                        if count == 3:
                            if sections != "":
                                items.append(sections)
                                sections={}
                                count=0
                                
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_faq_help", "model data", value_count, round(loadTime, 6))                     
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None 
            
            
    def resolve_get_chapter_check(self, info, course_id, user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_chapter_check', 'null')
            
            sections = {}
            items = []
            refId = []


            chapter_check = Table_data_info.objects.filter(table_id=27, column_data=course_id, user_id=user_id).order_by('table_ref_id')
            print("1315", chapter_check)

            for k in chapter_check:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))
            print("1321", refId)
            

            for m in refId:
                chapter_check_ref = Table_data_info.objects.filter(table_id=27, table_ref_id=m, user_id=user_id).order_by('table_ref_id')
                for i in chapter_check_ref:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==2:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            if sections != "":
                                items.append(sections)
                                sections={}
                                
            
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_chapter_check", "model data", value_count, round(loadTime, 6))                    
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None         
    
    def resolve_get_chapter(self, info, user_id, tab_rel_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_chapter', 'null')
            
            sections = {}
            items = []
            refId = []

            chapter_check_sections = {}
            

            chapter_data = Table_data_info.objects.filter(table_id=19, tab_rel_id=tab_rel_id).order_by('table_ref_id')
            
            
            count = 0
            for i in chapter_data:
                if i.table_col_id==1:
                    count+=1
                    sections[i.column_name]  = i.column_data
                    sections["chapter_id"]  = str(i.table_data_id)
                    chapter_check = Table_data_info.objects.filter(table_id=27, column_data=i.table_data_id, user_id=user_id).order_by('table_ref_id')
                    for k in chapter_check:
                        chapter_check_ref = Table_data_info.objects.filter(table_id=27, table_ref_id=k.table_ref_id, user_id=user_id).order_by('table_ref_id')
                        if chapter_check_ref:
                            for l in chapter_check_ref:
                                if l.table_col_id==1:
                                    chapter_check_sections[l.column_name]  = l.column_data
                                if l.table_col_id==2:
                                    chapter_check_sections[l.column_name]  = l.column_data
                                if l.table_col_id==3:
                                    chapter_check_sections[l.column_name]  = l.column_data
                                if l.table_col_id==4:
                                    chapter_check_sections[l.column_name]  = l.column_data
                            sections["chapter_check"]  = chapter_check_sections

                if i.table_col_id==2:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==3:
                    count+=1
                    sections[i.column_name]  = i.column_data
                    sections["table_id"]  = i.table_id
                    sections["table_ref_id"]  = i.table_ref_id
                # if i.table_col_id==4:
                #     count+=1
                #     sections[i.column_name]  = i.column_data
                #     sections["table_id"]  = i.table_id
                #     sections["table_ref_id"]  = i.table_ref_id

                if count == 2:    
                    if sections != "":
                        items.append(sections)
                        sections={}
                        chapter_check_sections={}   
                        count=0  
                        
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_chapter", "model data", value_count, round(loadTime, 6))             
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None 
    
    def resolve_get_chapter_content_dtl(self, info, tab_rel_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_chapter_content_dtl', 'null')
            
            sections = {}
            items = []
            refId = []

            chapter_check_sections = {}
            

            chapter_content_data = Table_data_info.objects.filter(table_id=20, tab_rel_id=tab_rel_id).order_by('table_ref_id')



            for k in chapter_content_data:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))


            for m in refId:
                for i in chapter_content_data:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==2:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
            if sections != "":
                items.append(sections)
                sections={}
                chapter_check_sections={} 
                
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_chapter_content_dtl", "model data", value_count, round(loadTime, 6))     
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
    
    def resolve_get_course(self, info, user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course', 'null')
            
            sections = {}
            items = []
            refId = []

            course_reg_sections = {}

            course_registration = Table_data_info.objects.filter(table_id=25, user_id=user_id).order_by('table_ref_id')


           
            count = 0
            for i in course_registration:
                if i.table_col_id==1:
                    count+=1
                    sections[i.column_name]  = i.column_data     
                if i.table_col_id==2:
                    count+=1
                    sections[i.column_name]  = i.column_data
                    course_data = Table_data_info.objects.get(table_id=18, table_data_id=i.column_data)
                    course_data_dtl = Table_data_info.objects.filter(table_id=18, table_ref_id=course_data.table_ref_id).order_by('table_ref_id')
                    if course_data_dtl:
                        for l in course_data_dtl:
                            course_reg_sections[l.column_name]  = l.column_data
                            course_reg_sections["table_id"]  = l.table_id
                            course_reg_sections["table_ref_id"]  = l.table_ref_id
                           
                            sections["course_data"]  = course_reg_sections

                if i.table_col_id==3:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==4:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==5:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==6:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==7:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==8:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==9:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==10:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==11:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==12:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==13:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==14:
                    count+=1
                    sections[i.column_name]  = i.column_data
                if i.table_col_id==15:
                    count+=1
                    sections[i.column_name]  = i.column_data
                    sections["table_id"]  = i.table_id
                    sections["table_ref_id"]  = i.table_ref_id
                    sections["user_id"]  = i.user_id

                if count == 15:
                    if sections != "":
                        items.append(sections)
                        sections={}
                        course_reg_sections={} 
                        count=0
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_course", "model data", value_count, round(loadTime, 6))                    
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
    
    def resolve_get_dummy_user_course(self, info, user_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_dummy_user_course', 'null')
            
            sections = {}
            items = []
            refId = []

            course_reg_sections = {}

            course_registration = Table_data_info.objects.filter(table_id=25, user_id=user_id).order_by('table_ref_id')

            
            if course_registration.count() == 0:
                course_data_dtl = Table_data_info.objects.filter(table_id=18).order_by('table_ref_id')
                if course_data_dtl:
                    count = 0
                    for l in course_data_dtl:

                        if l.table_col_id == 1:
                            count +=1 
                            course_reg_sections[l.column_name]  = l.column_data
                            course_reg_sections["course_id_table_data_id"]  = l.table_data_id
                        if l.table_col_id == 2:
                            count +=1 
                            course_reg_sections[l.column_name]  = l.column_data
                        if l.table_col_id == 3:
                            count +=1 
                            course_reg_sections[l.column_name]  = l.column_data
                        if l.table_col_id == 4:
                            count +=1 
                            course_reg_sections[l.column_name]  = l.column_data
                        if l.table_col_id == 5:
                            count +=1 
                            course_reg_sections[l.column_name]  = l.column_data
                            course_reg_sections["table_id"]  = l.table_id
                            course_reg_sections["table_ref_id"]  = l.table_ref_id
                        if count == 5:  
                            sections["course_data"]  = course_reg_sections
                            if sections != "":
                                items.append(sections)
                                sections={}
                                course_reg_sections={} 

           
           

                                   
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_dummy_user_course", "model data", value_count, round(loadTime, 6))  
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
    
    
    def resolve_get_course_complete_certificate(self, info, user_id, course_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_complete_certificate', 'null')
            
            sections = {}
            items = []
            refId = []

            course_reg_sections = {}
            course_sections = {}
            

            user_data = Table_data_info.objects.filter(table_id=1, user_id=user_id).order_by('table_ref_id')


            for k in user_data:
                refId.append(k.table_ref_id)
                   
            refId = list(set(refId))


            for m in refId:
                for i in user_data:
                    if i.table_ref_id==m:
                        if i.table_col_id==1:
                            sections[i.column_name]  = i.column_data
                            course_registration = Table_data_info.objects.get(table_data_id=course_id)
                            course_data = Table_data_info.objects.filter(table_id=18, user_id=course_registration.user_id, table_ref_id=course_registration.table_ref_id).order_by('table_ref_id')
                            if course_data:
                                for c in course_data:
                                    if c.table_col_id==1:
                                        course_sections[c.column_name]  = c.column_data
                                    if c.table_col_id==2:
                                        course_sections[c.column_name]  = c.column_data
                                    if c.table_col_id==3:
                                        course_sections[c.column_name]  = c.column_data
                                    if c.table_col_id==4:
                                        course_sections[c.column_name]  = c.column_data
                            course_registration_data = Table_data_info.objects.filter(table_id=25, user_id=course_registration.user_id, table_ref_id=course_registration.table_ref_id).order_by('table_ref_id')

                            if course_registration_data:
                                for l in course_registration_data:
                                    if l.table_col_id==1:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==2:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==3:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==4:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==5:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==6:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==7:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==8:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==9:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==10:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==11:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==12:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==13:
                                        course_reg_sections[l.column_name]  = l.column_data
                                    if l.table_col_id==14:
                                        course_reg_sections[l.column_name]  = l.column_data
                                
                                    
                        if i.table_col_id==2:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==3:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==4:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==5:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==6:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==7:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==8:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==9:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==10:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==11:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==12:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==13:
                            sections[i.column_name]  = i.column_data
                        if i.table_col_id==14:
                            sections[i.column_name]  = i.column_data
                            sections["table_id"]  = i.table_id
                            sections["table_ref_id"]  = i.table_ref_id
                            sections["course_reg"]  = course_reg_sections
                            sections["course"]  = course_sections
                            
                
                if sections != "":
                    items.append(sections)
                    sections={} 
                    course_reg_sections={}              
                    course_sections={} 
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_course_complete_certificate", "model data", value_count, round(loadTime, 6))         
            return GETMCQTableDataInfoType(mcq_data=items) 
        except Table_data_info.DoesNotExist:
            return None
    
    
    def resolve_get_course_progresbar(self, info, user_id, course_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_progresbar', 'null')
            course_data = Table_data_info.objects.get(table_id=25, user_id=user_id, column_data=course_id)
            course_dtl = Table_data_info.objects.filter(table_id=25, user_id=user_id, table_ref_id=course_data.table_ref_id).order_by('table_ref_id')
            if course_dtl:
                for i in course_dtl:
                    if i.table_col_id == 8:
                        endTime = CurrentTimeFunc()
                        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                        value_count = ValueCountFunc(i.column_data)
                        DataFetch_Static("get_course_progresbar", "model data", value_count, round(loadTime, 6))
                        return GETMCQTableDataInfoType(mcq_data=i.column_data) 
            
        except Table_data_info.DoesNotExist:
            return None 
            
    def resolve_get_exam_course_mcq_final_result(self, info, user_id, course_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_exam_course_mcq_final_result', 'null')
            
            course_data = Table_data_info.objects.get(table_id=25, user_id=user_id, column_data=course_id)
            course_dtl = Table_data_info.objects.filter(table_id=25, user_id=user_id, table_ref_id=course_data.table_ref_id)
            user_mcq_ans_data = Table_data_info.objects.filter(table_id=533, table_col_id=1, user_id=user_id, column_data=course_id)
            course_mcq_true_result_count=0
            for m in user_mcq_ans_data:
                course_mcq_true_result_count += Table_data_info.objects.filter(table_id=533, table_col_id=5, user_id=user_id, table_ref_id=m.table_ref_id, column_data="true").count()
            if course_dtl:
                for j in course_dtl:
                    if j.table_col_id == 15:
                        percentage_result = ((course_mcq_true_result_count*100)/(int(j.column_data)))
                        endTime = CurrentTimeFunc()
                        loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                        value_count = ValueCountFunc(int(percentage_result))
                        DataFetch_Static("get_exam_course_mcq_final_result", "model data", value_count, round(loadTime, 6))
                        return GETMCQTableDataInfoType(mcq_data=int(percentage_result))

        except Table_data_info.DoesNotExist:
            return None 
            
    def resolve_get_excel_file(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_excel_file', 'null')
            
            dataStore = {}
            columnName = []
            items = []

            # fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/excel/{currenttimedateE}.xlsx")
            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/excel/{currenttimedateE}.csv")

            if os.path.isfile(fileName):
                with open(fileName, 'r', encoding='utf-8') as file:
                    csvreader = csv.reader(file)
                    interestingrows=[row for idx, row in enumerate(csvreader) if 'Positions and Mark-to-Market Profit and Loss' in row]


                    for i in range(len(interestingrows)):
                        if i == 0:
                            for j in range(len(interestingrows[i])):
                                columnName.append(interestingrows[i][j])
                        if i != 0:
                            for k in range(len(interestingrows[i])):
                                for m in range(len(columnName)):
                                    if k == m:
                                        dataStore[columnName[m]]=interestingrows[i][k]

                            if dataStore != "":
                                items.append(dataStore)
                                dataStore={}

   
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(items)
                DataFetch_Static("get_excel_file", "model data", value_count, round(loadTime, 6))
                return GETMCQTableDataInfoType(mcq_data=items)
            else:
                return GETMCQTableDataInfoType(mcq_data="File is not found, Please Upload Your File") 
            
        except Table_data_info.DoesNotExist:
            return None        
    
    
    def resolve_get_yahoo_csv_file(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_yahoo_csv_file', 'null')
            
            dataStore = {}
            columnName = []
            items = []

            
            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/yahoo/AAPL.csv")

            if os.path.isfile(fileName):
                with open(fileName, 'r', encoding='utf-8') as file:
                    csvreader = csv.reader(file)
                    interestingrows=[row for idx, row in enumerate(csvreader)]

                    for i in range(len(interestingrows)):
                        if i == 0:
                            for j in range(len(interestingrows[i])):
                                columnName.append(interestingrows[i][j])
                        if i != 0:
                            for k in range(len(interestingrows[i])):
                                for m in range(len(columnName)):
                                    if k == m:
                                        dataStore[columnName[m]]=interestingrows[i][k]

                            if dataStore != "":
                                items.append(dataStore)
                                dataStore={}      

                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(items)
                DataFetch_Static("get_yahoo_csv_file", "model data", value_count, round(loadTime, 6))
                return GETMCQTableDataInfoType(mcq_data=items)
            else:
                return GETMCQTableDataInfoType(mcq_data="File is not found, Please Upload Your File") 
            
        except Table_data_info.DoesNotExist:
            return None
    
    
    def resolve_get_all_latest_news_json(self, info):
        try:
           
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_all_latest_news_json', 'null')
            
            AllNewsData = []
            dataSection = {}

            
            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/cnbc_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['cnbc_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['CNBC'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}

            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/apple_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['apple_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['APPLE'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}

            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/tesla_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['tesla_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['Tesla'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}

            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/c3ai_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['c3ai_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['C3ai'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}

            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/rivian_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['rivian_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['rivian'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}


            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/roku_news_data.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                news_array_data = data['roku_news_data']

                time = [x for x in news_array_data if currenttimedateE in x['time']] 
                dataSection['roku'] = time

                if dataSection != "":
                    AllNewsData.append(dataSection)
                    dataSection = {}


    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(AllNewsData)
            DataFetch_Static("get_all_latest_news_json", "model data", value_count, round(loadTime, 6))

            return GETMCQTableDataInfoType(mcq_data=AllNewsData)    
        except Table_data_info.DoesNotExist:
            return None
    
    
    
    def resolve_get_column_dtl(self, info, table_id):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_column_dtl', 'null')
            
            columnName = {}
            items = []

            column_dtl = Table_col_info.objects.filter(table_id=int(table_id))
            for i in column_dtl:
                columnName[i.table_col_id] = i.column_name

            if columnName != "":
                items.append(columnName)
                
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_column_dtl", "model data", value_count, round(loadTime, 6))    

            return GETMCQTableDataInfoType(mcq_data=items)
        except Table_data_info.DoesNotExist:
            return None
    
    
    def resolve_get_search_query(self, info, search=None, **kwargs):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_search_query', 'null')
            sections = {}
            items = []

            if search:
                 result = Table_data_info.objects.filter(Q(column_data__icontains=search))
                 for i in result:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 
                        
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_search_query", "model data", value_count, round(loadTime, 6))                
            return GETMCQTableDataInfoType(mcq_data=items)
        except Table_data_info.DoesNotExist:
            return None 
    
    def resolve_get_course_related_search(self, info, search=None, **kwargs):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_course_related_search', 'null')
            sections = {}
            items = []

            if search:
                table18_data = Table_data_info.objects.filter(table_id=18)
                table19_data = Table_data_info.objects.filter(table_id=19)
                table20_data = Table_data_info.objects.filter(table_id=20)
                table21_data = Table_data_info.objects.filter(table_id=21)
                table22_data = Table_data_info.objects.filter(table_id=22)
                table30_data = Table_data_info.objects.filter(table_id=30)
                table31_data = Table_data_info.objects.filter(table_id=31)
                
                result18 = table18_data.filter(Q(column_data__icontains=search))
                result19 = table19_data.filter(Q(column_data__icontains=search))
                result20 = table20_data.filter(Q(column_data__icontains=search))
                result21 = table21_data.filter(Q(column_data__icontains=search))
                result22 = table22_data.filter(Q(column_data__icontains=search))
                result30 = table30_data.filter(Q(column_data__icontains=search))
                result31 = table31_data.filter(Q(column_data__icontains=search))
               
                for i in result18:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

                for i in result19:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

                for i in result20:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={}

                for i in result21:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

                for i in result22:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

                for i in result30:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

                for i in result31:
                    sections['table_data_id']=i.table_data_id
                    sections['table_id']=i.table_id
                    sections['column_name']=i.column_name
                    sections['column_data']=i.column_data
                    if sections != "":
                        items.append(sections)
                        sections={} 

            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("get_course_related_search", "model data", value_count, round(loadTime, 6)) 
            return GETMCQTableDataInfoType(mcq_data=items)
        except Table_data_info.DoesNotExist:
            return None
            
            
    def resolve_get_cnbc_news(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_cnbc_news', 'null')
            data = requests.get(url="https://itb-usa.a2hosted.com/media/upload_file/json/cnbc_news_data.json/")
            cdata = data.json()
            item = cdata['cnbc_news_data']
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(item)
            DataFetch_Static("get_cnbc_news", "json data", value_count, round(loadTime, 6))
            return GETMCQTableDataInfoType(mcq_data=item)
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_node_design(self, info, name):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_node_design', 'null')
            
            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/node-design/{name}.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_node_design", "json data", value_count, round(loadTime, 6))
                return GETMCQTableDataInfoType(mcq_data=data)
            else:
                return GETMCQTableDataInfoType(mcq_data="File is not found, Please Upload Your File") 
            
        except Table_data_info.DoesNotExist:
            return None   
            
    def resolve_get_node_design_data(self, info, name):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_node_design_data', 'null')
            
            fileName = (f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/node-design/node_design.json")
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['node_design']
                compareValue = [x for x in array_data if name in x]
                endTime = CurrentTimeFunc()
                loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(compareValue)
                DataFetch_Static("get_node_design_data", "json data", value_count, round(loadTime, 6))
                return GETMCQTableDataInfoType(mcq_data=compareValue)
        except Table_data_info.DoesNotExist:
            return None
            
    def resolve_get_yahoo_info_file_name(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_yahoo_info_file_name', 'null')
            
            fileName = '/home/itbusaah/idriver_education_djangoproject/media/upload_file/yahoo_finance'
            dir_list = os.listdir(fileName)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(dir_list)
            DataFetch_Static("get_yahoo_info_file_name", "json data", value_count, round(loadTime, 6))
            return GETJSONFILEType(json_data=dir_list)
        except Table_data_info.DoesNotExist:
            return GETJSONFILEType(json_data="File name not found") 
            
    def resolve_get_yahoo_hist_file_name(self, info):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_yahoo_hist_file_name', 'null')
            fileName = main_media_url+'/media/upload_file/yahoo_finance_hist'
            dir_list = os.listdir(fileName)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(dir_list)
            DataFetch_Static("get_yahoo_hist_file_name", "json data", value_count, round(loadTime, 6))
            return GETJSONFILEType(json_data=dir_list)
        except Table_data_info.DoesNotExist:
            return GETJSONFILEType(json_data="File name not found")        
    
    def resolve_get_json_data_merge(self, info, api_key, codeFile, fileList):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('get_json_data_merge', 'null')
            exec(codeFile)
            datalist, success, error = ArrayJson(fileList)
            endTime = CurrentTimeFunc()
            loadTime = (datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(datalist)
            DataFetch_Static("get_json_data_merge", "json data", value_count, round(loadTime, 6))
            return GETJSONFILEType(json_data=datalist, success_message=success, error_message=error)
        except Table_data_info.DoesNotExist:
            return GETJSONFILEType(json_data="File name not found")
    
            
class UserValidation(graphene.Mutation):
    user_table_data_info = graphene.List(TableDataInfoType)
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        
    def mutate(self, info, email, password): 
        APICALLFUNCTION('UserValidation mutation', 'null')

        user = Table_data_info.objects.filter(table_id=4)
        if user.column_data==email and user.column_data==password:
            return True
        # else:
        #      raise Exception("fail") 
            
               
        
        # return UserValidation(message=f"success")     
        # return (user_table_data_info=user)        
        
 
 
class UserSignUp(graphene.Mutation):
    user_sign_up_table_data_info_email = graphene.Field(TableDataInfoType)
    user_sign_up_table_data_info_password = graphene.Field(TableDataInfoType)
    first_name_data = graphene.Field(TableDataInfoType)
    last_name_data = graphene.Field(TableDataInfoType)
    zipcode_data = graphene.Field(TableDataInfoType)
    role_data = graphene.Field(TableDataInfoType)
    is_email_verified = graphene.Field(TableDataInfoType)
    is_active = graphene.Field(TableDataInfoType)
    is_superuser = graphene.Field(TableDataInfoType)
    user_id = graphene.Field(TableDataInfoType)
    

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        
    def mutate(self, info, first_name, last_name, email, password):
        APICALLFUNCTION('UserSignUp mutation', 'null')
        
        user_count = Table_data_info.objects.filter(table_id=1).count()
        user_count_number = Table_data_info.objects.filter(column_name="user_id", table_id=1).count()
        if Table_data_info.objects.filter(column_data=email, table_id=1).exists():
            raise Exception("Email already exists.")
        userSignUpEmail = Table_data_info(table_id=1, table_col_id=1, user_id=user_count_number+1, column_data=email, table_ref_id=user_count+1, col_data_type="String", column_name='email') 
        userSignUpEmail.save()
        userSignUpPassword = Table_data_info(table_id=1, table_col_id=2, user_id=user_count_number+1, column_data=password, table_ref_id=user_count+1, col_data_type="String", column_name='password') 
        userSignUpPassword.save()
        userSignUpRole = Table_data_info(table_id=1, table_col_id=3, user_id=user_count_number+1, column_data="Driver", table_ref_id=user_count+1, col_data_type="String", column_name='role') 
        userSignUpRole.save()
        userSignUpIsActive = Table_data_info(table_id=1, table_col_id=4, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_active') 
        userSignUpIsActive.save()
        
        userSignUpIsSuperuser = Table_data_info(table_id=1, table_col_id=5, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_superuser') 
        userSignUpIsSuperuser.save()
        
        userSignUpEmailActivationFlag = Table_data_info(table_id=1, table_col_id=6, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_email_verified') 
        userSignUpEmailActivationFlag.save()
        
        userSignUpfirstname = Table_data_info(table_id=1, table_col_id=7, user_id=user_count_number+1, column_data=first_name, table_ref_id=user_count+1, col_data_type="String", column_name='first_name') 
        userSignUpfirstname.save()
        userSignUpLastName = Table_data_info(table_id=1, table_col_id=8, user_id=user_count_number+1, column_data=last_name, table_ref_id=user_count+1, col_data_type="String", column_name='last_name') 
        userSignUpLastName.save()
        userSignUpZipCode = Table_data_info(table_id=1, table_col_id=9, user_id=user_count_number+1, column_data="0", table_ref_id=user_count+1, col_data_type="String", column_name='zipcode') 
        userSignUpZipCode.save()
        userSignUpUserId = Table_data_info(table_id=1, table_col_id=10, user_id=user_count_number+1, column_data=user_count_number+1, table_ref_id=user_count+1, col_data_type="Int", column_name='user_id') 
        userSignUpUserId.save()
        
        send_activation_mail1(email, first_name)
        
            
        return UserSignUp(user_sign_up_table_data_info_email=userSignUpEmail, user_sign_up_table_data_info_password=userSignUpPassword, first_name_data=userSignUpfirstname, last_name_data=userSignUpLastName, role_data=userSignUpRole, zipcode_data=userSignUpZipCode, is_email_verified=userSignUpEmailActivationFlag, is_active=userSignUpIsActive, is_superuser=userSignUpIsSuperuser, user_id=userSignUpUserId) 
        
        
class UserSignUp1(graphene.Mutation):
    user_sign_up_table_data_info_email = graphene.Field(TableDataInfoType)
    user_sign_up_table_data_info_password = graphene.Field(TableDataInfoType)
    first_name_data = graphene.Field(TableDataInfoType)
    last_name_data = graphene.Field(TableDataInfoType)
    zipcode_data = graphene.Field(TableDataInfoType)
    role_data = graphene.Field(TableDataInfoType)
    is_email_verified = graphene.Field(TableDataInfoType)
    is_active = graphene.Field(TableDataInfoType)
    is_superuser = graphene.Field(TableDataInfoType)
    user_id = graphene.Field(TableDataInfoType)
    middle_name = graphene.Field(TableDataInfoType)
    dob = graphene.Field(TableDataInfoType)
    gender = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    address = graphene.Field(TableDataInfoType)
    city = graphene.Field(TableDataInfoType)
    state = graphene.Field(TableDataInfoType)
   
    

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
       
        
    def mutate(self, info, first_name, last_name, email, password):
        APICALLFUNCTION('UserSignUp1 mutation', 'null')
        
        user_count = Table_data_info.objects.filter(table_id=1).count()
        user_count_number = Table_data_info.objects.filter(column_name="user_id", table_id=1).count()
        if Table_data_info.objects.filter(column_data=email, table_id=1).exists():
            raise Exception("Email already exists.")
        userSignUpEmail = Table_data_info(table_id=1, table_col_id=1, user_id=user_count_number+1, column_data=email, table_ref_id=user_count+1, col_data_type="String", column_name='email') 
        userSignUpEmail.save()
        userSignUpPassword = Table_data_info(table_id=1, table_col_id=2, user_id=user_count_number+1, column_data=password, table_ref_id=user_count+1, col_data_type="String", column_name='password') 
        userSignUpPassword.save()
        userSignUpRole = Table_data_info(table_id=1, table_col_id=3, user_id=user_count_number+1, column_data="Invitation_User", table_ref_id=user_count+1, col_data_type="String", column_name='role') 
        userSignUpRole.save()
        userSignUpIsActive = Table_data_info(table_id=1, table_col_id=4, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_active') 
        userSignUpIsActive.save()
        
        userSignUpIsSuperuser = Table_data_info(table_id=1, table_col_id=5, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_superuser') 
        userSignUpIsSuperuser.save()
        
        userSignUpEmailActivationFlag = Table_data_info(table_id=1, table_col_id=6, user_id=user_count_number+1, column_data="False", table_ref_id=user_count+1, col_data_type="Boolean", column_name='is_email_verified') 
        userSignUpEmailActivationFlag.save()
        
        userSignUpfirstname = Table_data_info(table_id=1, table_col_id=7, user_id=user_count_number+1, column_data=first_name, table_ref_id=user_count+1, col_data_type="String", column_name='first_name') 
        userSignUpfirstname.save()
        userSignUpLastName = Table_data_info(table_id=1, table_col_id=8, user_id=user_count_number+1, column_data=last_name, table_ref_id=user_count+1, col_data_type="String", column_name='last_name') 
        userSignUpLastName.save()
        userSignUpZipCode = Table_data_info(table_id=1, table_col_id=9, user_id=user_count_number+1, column_data="0", table_ref_id=user_count+1, col_data_type="String", column_name='zipcode') 
        userSignUpZipCode.save()
        userSignUpUserId = Table_data_info(table_id=1, table_col_id=10, user_id=user_count_number+1, column_data=user_count_number+1, table_ref_id=user_count+1, col_data_type="Int", column_name='user_id') 
        userSignUpUserId.save()
        middle_name = Table_data_info(table_id=1, table_col_id=11, user_id=user_count_number+1, column_data="A", table_ref_id=user_count+1, col_data_type="String", column_name='middle_name') 
        middle_name.save()
        dob = Table_data_info(table_id=1, table_col_id=12, user_id=user_count_number+1, column_data="dob", table_ref_id=user_count+1, col_data_type="datetimefield", column_name='dob') 
        dob.save()
        gender = Table_data_info(table_id=1, table_col_id=13, user_id=user_count_number+1, column_data="Male", table_ref_id=user_count+1, col_data_type="string", column_name='gender') 
        gender.save()
        phone_number = Table_data_info(table_id=1, table_col_id=14, user_id=user_count_number+1, column_data="phone_number", table_ref_id=user_count+1, col_data_type="string", column_name='phone_number') 
        phone_number.save()
        address = Table_data_info(table_id=1, table_col_id=15, user_id=user_count_number+1, column_data="address", table_ref_id=user_count+1, col_data_type="string", column_name='address') 
        address.save()
        city = Table_data_info(table_id=1, table_col_id=16, user_id=user_count_number+1, column_data="city", table_ref_id=user_count+1, col_data_type="string", column_name='city') 
        city.save()
        state = Table_data_info(table_id=1, table_col_id=17, user_id=user_count_number+1, column_data="state", table_ref_id=user_count+1, col_data_type="string", column_name='state') 
        state.save()
        
        
        send_activation_mail1(email, first_name)
        
            
        return UserSignUp1(
            user_sign_up_table_data_info_email=userSignUpEmail, 
            user_sign_up_table_data_info_password=userSignUpPassword, 
            first_name_data=userSignUpfirstname, 
            last_name_data=userSignUpLastName, 
            role_data=userSignUpRole, 
            zipcode_data=userSignUpZipCode, 
            is_email_verified=userSignUpEmailActivationFlag, 
            is_active=userSignUpIsActive, 
            is_superuser=userSignUpIsSuperuser, 
            user_id=userSignUpUserId, 
            middle_name=middle_name, 
            dob=dob, 
            gender=gender,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state
        )         
        
        


import math, random

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(8) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP 

import datetime;
def CurrentTimeStand():
    ct = datetime.datetime.now()
    return ct        
        
class UserSignIn(graphene.Mutation): 
    result = graphene.Boolean()
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        
    def mutate(self, info, email, password):
        
        APICALLFUNCTION('UserSignIn mutation', 'null')
        
        email_detail = Table_data_info.objects.get(column_data=email, table_id=1)
        password_detail = Table_data_info.objects.get(table_id=1, table_ref_id=email_detail.table_ref_id, column_data=password, user_id=email_detail.user_id, column_name='password')
           
        if email_detail.table_ref_id==password_detail.table_ref_id and email_detail.user_id==password_detail.user_id:
            flag_check = Table_data_info.objects.filter(table_ref_id=email_detail.table_ref_id, user_id=email_detail.user_id, table_id=1)

            email_active = []
            user_active = []
            for i in flag_check:
                if i.column_name=="is_email_verified" and i.column_data=="True" and i.table_ref_id==email_detail.table_ref_id and i.user_id==email_detail.user_id and i.table_col_id==6:
                    email_active.append(i.column_data)
                if i.column_name=="is_active" and i.column_data=="True" and i.table_ref_id==email_detail.table_ref_id and i.user_id==email_detail.user_id and i.table_col_id==4:
                    user_active.append(i.column_data)
                                 
            if email_active and user_active:
                if email_active[0]=="True" and user_active[0]=="True":
                    user_otp=generateOTP()
                    cts = CurrentTimeStand()
                    if Table_data_info.objects.filter(column_data=email, user_id=email_detail.user_id, table_id=2).exists():
                        otp_check_email = Table_data_info.objects.get(column_data=email, user_id=email_detail.user_id, table_id=2)
                        otp_check = Table_data_info.objects.filter(table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id, table_id=2)
                        count = 0
                        for i in otp_check:
                            if i.table_id==2 and i.table_col_id==2 and i.column_name=="user_otp" and i.table_ref_id==otp_check_email.table_ref_id and i.user_id==otp_check_email.user_id:
                                otp_update = Table_data_info.objects.get(table_id=i.table_id, table_col_id=i.table_col_id, column_name=i.column_name, table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id)
                                otp_update.column_data=user_otp
                                otp_update.save()
                                count=count+1
                                
                                
                            if i.table_id==2 and i.table_col_id==3 and i.column_name=="timestamp" and i.table_ref_id==otp_check_email.table_ref_id and i.user_id==otp_check_email.user_id:
                                cts_update = Table_data_info.objects.get(table_id=i.table_id, table_col_id=i.table_col_id, column_name=i.column_name, table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id)
                                cts_update.column_data=cts
                                cts_update.save()
                                count=count+1
                            
                            if count == 2:
                                send_user_otp_mail(email, user_otp, cts)
                                return UserSignIn(result=True)    
                            
                    else:    
                        userPassDetailEmail = Table_data_info(table_id=2, table_col_id=1, user_id=email_detail.user_id, column_data=email, table_ref_id=email_detail.table_ref_id, col_data_type="String", column_name='user_email') 
                        userPassDetailEmail.save()
                        userPassDetailOtp = Table_data_info(table_id=2, table_col_id=2, user_id=email_detail.user_id, column_data=user_otp, table_ref_id=email_detail.table_ref_id, col_data_type="String", column_name='user_otp') 
                        userPassDetailOtp.save()
                        userPassDetailCTS = Table_data_info(table_id=2, table_col_id=3, user_id=email_detail.user_id, column_data=cts, table_ref_id=email_detail.table_ref_id, col_data_type="DateTimeField", column_name='timestamp') 
                        userPassDetailCTS.save()
                        userPassDetailToken = Table_data_info(table_id=2, table_col_id=4, user_id=email_detail.user_id, column_data='tokenabc', table_ref_id=email_detail.table_ref_id, col_data_type="String", column_name='user_token') 
                        userPassDetailToken.save()
                        
        
                        JsonLogFile(current_time)
                        
                        return UserSignIn(result=True)
                else:
                    return UserSignIn(result=False)
            else:
                return UserSignIn(result=False)                   
    
    
class UserOTPCheck(graphene.Mutation): 
    result = graphene.Boolean()
    token = graphene.String()
    # login = graphene.List(TableDataInfoType)
    class Arguments:
        email = graphene.String(required=True)
        user_otp = graphene.String(required=True)

    def mutate(self, info, email , user_otp):
        try:
            
            # APICALLFUNCTION('UserOTPCheck mutation', 'null')
            
            user_email_otp = Table_data_info.objects.get(table_id=2, table_col_id=1, column_data=email)
            user_otp_check = Table_data_info.objects.get(table_id=2, table_col_id=2, table_ref_id=user_email_otp.table_ref_id, column_data=user_otp, user_id=user_email_otp.user_id)
            if user_email_otp.table_ref_id==user_otp_check.table_ref_id and user_email_otp.user_id==user_otp_check.user_id and user_otp_check.column_data==user_otp:
                email_detail = Table_data_info.objects.get(table_id=1, column_data=email)
                login = Table_data_info.objects.filter(table_id=1, table_ref_id=email_detail.table_ref_id, user_id=email_detail.user_id)
                # print("login", login)
                login_data = {}
                for m in login:
                    # print("m", m.column_name, m.column_data)
                    if m.column_name == 'user_id':
                        login_data['pk'] = m.pk
                        login_data[m.column_name] = m.column_data
                    login_data[m.column_name] = m.column_data

                # login_data1.append(login_data)
                print("login_data", login_data)
                # print("TokenGen",  TokenGen(login_data))
                
                # print("TokenGen",  JWTTokenGenerator.generate_token(login_data))
                # print("TokenGen",  get_tokens_for_user(email_detail))
                token = JWTTokenGenerator.generate_token(login_data)
                user_token_update = Table_data_info.objects.get(table_id=2, table_col_id=4, column_name='user_token', user_id=email_detail.user_id)
                user_token_update.column_data=token
                user_token_update.save()
                return UserOTPCheck(result=True, token=token)
                # return UserOTPCheck(result=True, login=login)
            else:
                return UserOTPCheck(result=False)
        except Table_data_info.DoesNotExist:
            return UserOTPCheck(result=False)
            
            
class CreateCourseInfoDynamic(graphene.Mutation): 
    course_id = graphene.Field(TableDataInfoType)
    course_desc = graphene.Field(TableDataInfoType)
    course_short_desc = graphene.Field(TableDataInfoType)
    course_length = graphene.Field(TableDataInfoType)
    class Arguments:
        course_desc = graphene.String(required=True)
        course_short_desc = graphene.String(required=True)
        course_length = graphene.String(required=True)
        
    def mutate(self, info, course_desc, course_short_desc, course_length):
        try:
            APICALLFUNCTION('CreateCourseInfoDynamic', 'null')
            
            table_ref_id_count = Table_data_info.objects.filter(table_id=13).count()
            print("123", table_ref_id_count+1)
            course_id_count = Table_data_info.objects.filter(table_id=13, column_name="course_id").count()
            print("123", course_id_count+1)
            course_id = Table_data_info(table_id=13, table_col_id=1, column_data=course_id_count+1, table_ref_id=table_ref_id_count+1, col_data_type="AutoField", column_name='course_id') 
            course_id.save()
            course_desc = Table_data_info(table_id=13, table_col_id=2, column_data=course_desc, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='course_desc') 
            course_desc.save()
            course_short_desc = Table_data_info(table_id=13, table_col_id=3, column_data=course_short_desc, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='course_short_desc') 
            course_short_desc.save()
            course_length = Table_data_info(table_id=13, table_col_id=4, column_data=course_length, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='course_length') 
            course_length.save()
            return CreateCourseInfoDynamic(course_id=course_id, course_desc=course_desc, course_short_desc=course_short_desc, course_length=course_length)
        except Table_data_info.DoesNotExist:
            return None
            
            
            
class CreateUserCourseMcqResultDynamic(graphene.Mutation): 
    user_id = graphene.Field(TableDataInfoType)
    question_id = graphene.Field(TableDataInfoType)
    result = graphene.Field(TableDataInfoType)
    class Arguments:
        userid = graphene.String(required=True)
        question_id = graphene.String(required=True)
        result = graphene.String(required=True)
        
    def mutate(self, info, userid, question_id, result):
        try:
            APICALLFUNCTION('CreateUserCourseMcqResultDynamic mutation', 'null')
            table_ref_id_count = Table_data_info.objects.filter(table_id=11).count()
            print("852", table_ref_id_count+1)
            
            userid = Table_data_info(table_id=11, table_col_id=1, column_data=userid, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='userid') 
            userid.save()
            question_id = Table_data_info(table_id=11, table_col_id=2, column_data=question_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='question_id') 
            question_id.save()
            result = Table_data_info(table_id=11, table_col_id=3, column_data=result, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='result') 
            result.save()
            
            return CreateUserCourseMcqResultDynamic(user_id=userid, question_id=question_id, result=result)
        except Table_data_info.DoesNotExist:
            return None                        
           

class ContentBodyInput(graphene.InputObjectType):
    contents_body = graphene.String(required=True)
                   
class McqDetailInput(graphene.InputObjectType):
    mcq_choice = graphene.String(required=True)
    mcq_choice_slno = graphene.String(required=True)
    mcq_choice_type = graphene.String()
    mcq_q_image_url = graphene.String()
    
class CreateCourse(graphene.Mutation):
    course_info = graphene.Field(CourseInfoType)
    content_description_master = graphene.Field(ContentDescriptionMasterType)
    content_description_detail = graphene.List(ContentDescriptionDetailType)
    content_mcq_master = graphene.Field(ContentMcqMasterType)
    content_mcq_detail = graphene.List(ContentMcqDetailType)
    
    
    class Arguments:
        course_desc = graphene.String(required=True)
        course_short_desc = graphene.String(required=True)
        course_length = graphene.Float(required=True)
        
        ccon_desc_title = graphene.String(required=True)
        ccon_desc_sub_title = graphene.String(required=True)
        
        contents_body = graphene.List(ContentBodyInput)
        
        mcq_question = graphene.String(required=True)
        mcq_q_multi = graphene.Boolean(required=True)
        
        mcq_detail = graphene.List(McqDetailInput)
        
        
    def mutate(self, info, course_desc, course_short_desc, course_length, ccon_desc_title, ccon_desc_sub_title, mcq_question, mcq_q_multi, contents_body, mcq_detail):
        
        APICALLFUNCTION('CreateCourse mutation', 'null')
        
        courseinfo = course_info(course_desc=course_desc, course_short_desc=course_short_desc, course_length=course_length) 
        courseinfo.save() 
        
        contentdescriptionmaster = ccon_desc_master(ccon_desc_title=ccon_desc_title, ccon_desc_sub_title=ccon_desc_sub_title) 
        contentdescriptionmaster.save()
        
        contentdescriptiondetail = [ccon_desc_dtl.objects.create(cdm_id=contentdescriptionmaster, **data) for data in contents_body ]
        
        contentmcqmaster = ccon_mcq_mst(cdm_id=contentdescriptionmaster, mcq_question=mcq_question, mcq_q_multi=mcq_q_multi)
        contentmcqmaster.save()
        
        contentmcqdetail = [ccon_mcq_dtl.objects.create(mcq_id=contentdescriptionmaster, **data) for data in mcq_detail ]
        
        
        
        return CreateCourse(course_info=courseinfo, content_description_master=contentdescriptionmaster, content_description_detail=contentdescriptiondetail, content_mcq_master=contentmcqmaster, content_mcq_detail=contentmcqdetail)


class CreateCourseMaster(graphene.Mutation):
    course_info = graphene.Field(CourseInfoType)
    content_description_master = graphene.Field(ContentDescriptionMasterType)
    content_mcq_master = graphene.Field(ContentMcqMasterType)
   
    class Arguments:
        course_desc = graphene.String(required=True)
        course_short_desc = graphene.String(required=True)
        course_length = graphene.String(required=True)
        
        ccon_desc_title = graphene.String(required=True)
        ccon_desc_sub_title = graphene.String(required=True)

        
        mcq_question = graphene.String(required=True)
        mcq_q_multi = graphene.Boolean(required=True)
        
        
    def mutate(self, info, course_desc, course_short_desc, course_length, ccon_desc_title, ccon_desc_sub_title, mcq_question, mcq_q_multi):
        
        APICALLFUNCTION('CreateCourseMaster mutation', 'null')
        
        courseinfo = course_info(course_desc=course_desc, course_short_desc=course_short_desc, course_length=course_length) 
        courseinfo.save() 
        
        contentdescriptionmaster = ccon_desc_master(ccon_desc_title=ccon_desc_title, ccon_desc_sub_title=ccon_desc_sub_title) 
        contentdescriptionmaster.save()
                
        contentmcqmaster = ccon_mcq_mst(cdm_id=contentdescriptionmaster, mcq_question=mcq_question, mcq_q_multi=mcq_q_multi)
        contentmcqmaster.save()
        
        return CreateCourseMaster(course_info=courseinfo, content_description_master=contentdescriptionmaster, content_mcq_master=contentmcqmaster)
        
        
class CreateCourseInfo(graphene.Mutation):
    course_info = graphene.Field(CourseInfoType)
    
    class Arguments:
        course_desc = graphene.String(required=True)
        course_short_desc = graphene.String(required=True)
        course_length = graphene.String(required=True)
        
    def mutate(self, info, course_desc, course_short_desc, course_length):
        APICALLFUNCTION('CreateCourseInfo mutation', 'null')
        courseinfo = course_info(course_desc=course_desc, course_short_desc=course_short_desc, course_length=course_length) 
        courseinfo.save()
            
        return CreateCourseInfo(course_info=courseinfo)
        
        
def JsonData(tab_id, col_id, tab_rel_id, column_data):
    # function to add to JSON
    def write_json(new_data, filename='/home/itbusaah/idrivereducation/courseapp/tabledatainfo.json'):
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["data"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    
        # python object to be appended
    y = {
        "tab_id":tab_id,
        "col_id": col_id,
        "tab_rel_id": tab_rel_id,
        "column_data": column_data,
        }
        
    write_json(y)


class TableDataJson(graphene.Mutation):
    table_data_info = graphene.Field(TableDataJsonInfoType)
    class Arguments:
        tab_id = graphene.Int(required=True)  
        col_id = graphene.Int(required=True)  
        tab_rel_id = graphene.Int(required=True)  
        column_data = graphene.String(required=True)  
    
    def mutate(self, info, tab_id, col_id, tab_rel_id, column_data):
        APICALLFUNCTION('TableDataJson mutation', 'null')
        data_value = JsonData(tab_id, col_id, tab_rel_id, column_data)
        return data_value          
    
      
class CreateTableDataInfo(graphene.Mutation):
    table_data_info = graphene.Field(TableDataInfoType)
    
    class Arguments:
        table_id = graphene.Int(required=True)
        table_col_id = graphene.Int(required=True)
        tab_rel_id = graphene.String()
        column_data = graphene.String(required=True)
        
        
    def mutate(self, info, table_id, table_col_id, tab_rel_id, column_data):
        APICALLFUNCTION('CreateTableDataInfo mutation', 'null')
        count_data = Table_data_info.objects.filter(table_id=table_id).count()
        # table_id = Table_info_dtl.objects.get(id=table_id)
        # table_col_id = Table_col_info.objects.get(id=table_col_id)
        if tab_rel_id:
	        Tabledatainfo = Table_data_info(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id, table_ref_id=count_data+1, column_data=column_data, col_data_type="String", column_name='a') 
	        Tabledatainfo.save()
	            
	        return CreateTableDataInfo(table_data_info=Tabledatainfo) 

class CRUDInfo(graphene.Mutation):
    table_data_info = graphene.Field(TableDataInfoType)
    
    class Arguments:
        table_id = graphene.Int(required=True)
        table_col_id = graphene.Int(required=True)
        table_ref_id = graphene.Int(required=True)
        tab_rel_id = graphene.String(required=True)
        column_data = graphene.String(required=True)
        column_name = graphene.String(required=True)
        user_id = graphene.String(required=True)
        
        
    def mutate(self, info, table_id, table_col_id, table_ref_id, tab_rel_id, column_data, user_id, column_name):
        APICALLFUNCTION('CRUDInfo mutation', 'null')
        Tabledatainfo = Table_data_info(table_id=table_id, table_col_id=table_col_id, table_ref_id=table_ref_id, tab_rel_id=tab_rel_id, column_data=column_data,  user_id=user_id, col_data_type="null", column_name=column_name) 
        Tabledatainfo.save()    
        return CreateTableDataInfo(table_data_info=Tabledatainfo) 	        
	        
    
    
class CRUDInfoUserId(graphene.Mutation):
    table_data_info = graphene.Field(TableDataInfoType)
    
    class Arguments:
        table_id = graphene.Int(required=True)
        table_col_id = graphene.Int(required=True)
        table_ref_id = graphene.Int(required=True)
        tab_rel_id = graphene.String(required=True)
        column_data = graphene.String(required=True)
        user_id = graphene.String(required=True)
        
        
    def mutate(self, info, table_id, table_col_id, table_ref_id, tab_rel_id, column_data, user_id):
        APICALLFUNCTION('CRUDInfoUserId mutation', 'null')
        Tabledatainfo = Table_data_info(table_id=table_id, user_id=user_id, table_col_id=table_col_id, table_ref_id=table_ref_id, tab_rel_id=tab_rel_id, column_data=column_data, col_data_type="null", column_name='null') 
        Tabledatainfo.save()    
        return CreateTableDataInfo(table_data_info=Tabledatainfo)    
    

class CreateTableColInfo(graphene.Mutation):
    Table_col_info = graphene.Field(TableColInfoType)  
    
    class Arguments:
        col_desc = graphene.String(required=True)  
        column_name = graphene.String(required=True)  
        col_data_type = graphene.String(required=True)  
        table_col_id = graphene.Int(required=True)  
        col_classi = graphene.String(required=True)  
        
    def mutate(self, info, col_desc, column_name, col_data_type, table_col_id, col_classi):
        APICALLFUNCTION('CreateTableColInfo mutation', 'null')
        Tablecolinfo = Table_col_info(table_id=2, col_desc=col_desc, column_name=column_name, col_data_type=col_data_type, table_col_id=table_col_id, col_classi=col_classi) 
        Tablecolinfo.save()      
        
        TableColInfoSubcription.broadcast(payload={'id': Tablecolinfo.id, 'col_desc': Tablecolinfo.col_desc, 'column_name': Tablecolinfo.column_name })
        
        return CreateTableColInfo(Table_col_info=Tablecolinfo) 


class TableColInfoSubcription(channels_graphql_ws.Subscription):
    Table_col_info = graphene.Field(TableColInfoType)
    payload = graphene.JSONString() 
    
    # class Arguments:
    #     name = graphene.String(required=True)  
        
    @staticmethod
    def subscribe(root, info):  
        pass  
        # return [name] if name is not None else None
    
    @staticmethod
    def publish(payload, info):
        APICALLFUNCTION('TableColInfoSubcription subcription', 'null')
        print(payload)
        Tablecolinfo = Table_col_info.objects.get(id=payload['id'])
        return TableColInfoSubcription(payload=payload, Table_col_info=Tablecolinfo)
      
  
class CreateEventInvitationDynamic(graphene.Mutation):
    event_title = graphene.Field(TableDataInfoType)
    start_date_and_time = graphene.Field(TableDataInfoType)
    bbt = graphene.Field(TableDataInfoType)
    engagement = graphene.Field(TableDataInfoType)
    hosted_by = graphene.Field(TableDataInfoType)
    location = graphene.Field(TableDataInfoType)
    host_phone_number = graphene.Field(TableDataInfoType)
    message = graphene.Field(TableDataInfoType)
    event_image = graphene.Field(TableDataInfoType)

    
    class Arguments:
        event_title = graphene.String(required=True)
        start_date_and_time = graphene.String(required=True)
        bbt = graphene.String(required=True)
        engagement = graphene.String(required=True)
        hosted_by = graphene.String(required=True)
        location = graphene.String(required=True)
        host_phone_number = graphene.String(required=True)
        message = graphene.String(required=True)
        extension = graphene.String(required=True)
        event_user_id = graphene.String(required=True)
        
    def mutate(self, info, event_title, start_date_and_time, bbt, engagement, hosted_by, location, host_phone_number, message, extension, event_user_id):
        APICALLFUNCTION('CreateEventInvitationDynamic subcription', 'null')
        # invitation_image = InvitationEventUploadFile.objects.all().last()
        # invitation_image = InvitationEventUploadFile.objects.get(name=event_title)
        # print("1386", invitation_image)
        # print("1387", invitation_image.file_name)
        # print("1388", invitation_image.file_name.url )
        
        image_file_name = slugify(event_title)
        image_file_date = slugify(bbt)
        print("1406", image_file_name)
        image_file_extension = f"/media/upload_file/invitation_event/images/{image_file_name}{image_file_date}{extension}"
        if Table_data_info.objects.filter(table_id=4, user_id=event_user_id, column_data=event_title).exists():
            if Table_data_info.objects.filter(table_id=4, user_id=event_user_id, column_data=bbt).exists():
                raise Exception("This name of event is already created.")
        
        table_ref_id_count = Table_data_info.objects.filter(table_id=4).count()
        print("1195", table_ref_id_count+1)
    
        eventTitle = Table_data_info(table_id=4, table_col_id=1, user_id=event_user_id, column_data=event_title, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='event_title') 
        eventTitle.save()
        print("1199")
        startDateAndTime = Table_data_info(table_id=4, table_col_id=2, user_id=event_user_id, column_data=start_date_and_time, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='start_date_and_time') 
        startDateAndTime.save()
        print("1202")
        bbt = Table_data_info(table_id=4, table_col_id=3, user_id=event_user_id, column_data=bbt, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='bbt') 
        bbt.save()
        engagement = Table_data_info(table_id=4, table_col_id=4, user_id=event_user_id, column_data=engagement, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='engagement') 
        engagement.save()
        hostedBy = Table_data_info(table_id=4, table_col_id=5, user_id=event_user_id, column_data=hosted_by, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='hosted_by') 
        hostedBy.save()
        location = Table_data_info(table_id=4, table_col_id=6, user_id=event_user_id, column_data=location, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='location') 
        location.save()
        hostPhoneNumber = Table_data_info(table_id=4, table_col_id=7, user_id=event_user_id, column_data=host_phone_number, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='host_phone_number') 
        hostPhoneNumber.save()
        message = Table_data_info(table_id=4, table_col_id=8, user_id=event_user_id, column_data=message, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='message') 
        message.save()
        event_image = Table_data_info(table_id=4, table_col_id=9, user_id=event_user_id, column_data=image_file_extension, table_ref_id=table_ref_id_count+1, col_data_type="URLField", column_name='event_image_url') 
        event_image.save()
        
        table_ref_id_count_event = Table_data_info.objects.filter(table_id=5).count()
        user_contact = Table_data_info.objects.filter(table_id=6, user_id=event_user_id)
        
        counti = 1
        
        event_title_detail1 = Table_data_info.objects.filter(table_id=4,  user_id=event_user_id, column_data=event_title)
        if event_title_detail1:
            for k in event_title_detail1:
                if Table_data_info.objects.filter(table_id=4,  user_id=event_user_id, column_data=bbt, table_ref_id=k.table_ref_id).exists():
                    event_title_detail = Table_data_info.objects.get(table_id=4, user_id=event_user_id, column_data=event_title, table_ref_id=k.table_ref_id)
                    if user_contact:
                        for i in user_contact:
                            if i.column_name=='first_name':
                                event_first_name = Table_data_info(table_id=5, table_col_id=1, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=i.column_data, table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='first_name') 
                                event_first_name.save()
                            if i.column_name=='last_name':
                                event_last_name = Table_data_info(table_id=5, table_col_id=2, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=i.column_data, table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='last_name') 
                                event_last_name.save()
                            if i.column_name=='email':
                                event_email = Table_data_info(table_id=5, table_col_id=3, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=i.column_data, table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='email') 
                                event_email.save()
                            if i.column_name=='zipcode':
                                event_zipcode = Table_data_info(table_id=5, table_col_id=4, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=i.column_data, table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='zipcode') 
                                event_zipcode.save()
                            if i.column_name=='phone_number':
                                event_phone_number = Table_data_info(table_id=5, table_col_id=5, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=i.column_data, table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='phone_number') 
                                event_phone_number.save()
                                event_check_box = Table_data_info(table_id=5, table_col_id=6, user_id=event_user_id, tab_rel_id=event_title_detail.table_data_id, column_data="True", table_ref_id=table_ref_id_count_event+counti, col_data_type="String", column_name='check_box') 
                                event_check_box.save()
                                counti = counti + 6
        

            
        return CreateEventInvitationDynamic(event_title=eventTitle, start_date_and_time=startDateAndTime, bbt=bbt, engagement=engagement, hosted_by=hostedBy, location=location, host_phone_number=hostPhoneNumber, message=message, event_image=event_image)

        
        
class DeleteRecord(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        APICALLFUNCTION('DeleteRecord mutation', 'null')
        record = Table_data_info.objects.get(table_data_id=id)
        record.delete()
        return DeleteRecord(message=f"{id} id is Deleted") 
        
class column_data_delete(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        APICALLFUNCTION('column_data_delete mutation', 'null')
        record = Table_data_info.objects.get(table_data_id=id)
        record.delete()
        return column_data_delete(message=f"{id} id is Deleted") 
        
        
class column_data_update(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        column_data = graphene.String(required=True)

    def mutate(self, info, id, column_data):
        APICALLFUNCTION('column_data_update mutation', 'null')
        record = Table_data_info.objects.get(table_data_id=id)
        record.column_data=column_data
        record.save()
        return column_data_delete(message=f"{id} id is Updated") 
        
        
class ImageUpload(graphene.Mutation):
    admin_files_url = graphene.Field(TableDataInfoType)

    class Arguments:
        name = graphene.String(required=True)
        date = graphene.String(required=True)
        extension = graphene.String(required=True)
        user_id = graphene.String(required=True)
        
    def mutate(self, info, name, date, extension, user_id):
        APICALLFUNCTION('ImageUpload mutation', 'null')
        image_file_name = slugify(name)
        image_file_date = slugify(date)
        image_file_extension = f"/media/upload_file/images/{image_file_name}{image_file_date}{extension}"
        
        table_ref_id_count = Table_data_info.objects.filter(table_id=16).count()

        admin_files_url = Table_data_info(table_id=16, table_col_id=1, user_id=user_id, column_data=image_file_extension, table_ref_id=table_ref_id_count+1, col_data_type="URLField", column_name='admin_files_url') 
        admin_files_url.save()

        return ImageUpload(admin_files_url=admin_files_url)        
        
        
class AddContact(graphene.Mutation):
    first_name = graphene.Field(TableDataInfoType)
    last_name = graphene.Field(TableDataInfoType)
    email = graphene.Field(TableDataInfoType)
    zipcode = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    event_first_name = graphene.Field(TableDataInfoType)
    event_last_name = graphene.Field(TableDataInfoType)
    event_email = graphene.Field(TableDataInfoType)
    event_zipcode = graphene.Field(TableDataInfoType)
    event_phone_number = graphene.Field(TableDataInfoType)
    event_check_box = graphene.Field(TableDataInfoType)
    
    
    
    # message = graphene.Field(Message)
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        zipcode = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        event_contact_user_id = graphene.String(required=True)
        event_title = graphene.String(required=True)
        bbt = graphene.String(required=True)
        
    def mutate(self, info, first_name, last_name, email, zipcode, phone_number, event_contact_user_id, event_title, bbt):
        APICALLFUNCTION('AddContact mutation', 'null')
        
        table_ref_id_count = Table_data_info.objects.filter(table_id=6).count()
        table_ref_id_count_event = Table_data_info.objects.filter(table_id=5).count()
        print("123", table_ref_id_count+1)
        
        event_title_detail1 = Table_data_info.objects.filter(table_id=4, user_id=event_contact_user_id, column_data=event_title)
        
        if event_title_detail1:
            for k in event_title_detail1:
                if Table_data_info.objects.filter(table_id=4,  user_id=event_contact_user_id, column_data=bbt, table_ref_id=k.table_ref_id).exists():
                    event_title_detail = Table_data_info.objects.get(table_id=4, user_id=event_contact_user_id, column_data=event_title, table_ref_id=k.table_ref_id)
                    event_contact_title_detail = Table_data_info.objects.filter(table_id=5, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id).last()
                    
                    if Table_data_info.objects.filter(column_data=email, table_id=6, user_id=event_contact_user_id).exists():
                        raise Exception("Email already exists User Contact.")
                    if Table_data_info.objects.filter(column_data=phone_number, table_id=6, user_id=event_contact_user_id).exists():
                        raise Exception("Phone Number already exists User Contact.")
                    
                        
                    if event_contact_title_detail:
                        if Table_data_info.objects.filter(column_data=email, table_id=5, table_ref_id=event_contact_title_detail.table_ref_id).exists():
                            raise Exception("Email already exists Event Contact.")
                        if Table_data_info.objects.filter(column_data=phone_number, table_id=5, table_ref_id=event_contact_title_detail.table_ref_id).exists():
                            raise Exception("Phone Number already exists Event Contact.")
                            
                        first_name = Table_data_info(table_id=6, table_col_id=1, user_id=event_contact_user_id, column_data=first_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='first_name') 
                        first_name.save()
                        last_name = Table_data_info(table_id=6, table_col_id=2, user_id=event_contact_user_id, column_data=last_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='last_name') 
                        last_name.save()
                        email = Table_data_info(table_id=6, table_col_id=3, user_id=event_contact_user_id, column_data=email, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='email') 
                        email.save()
                        zipcode = Table_data_info(table_id=6, table_col_id=4, user_id=event_contact_user_id, column_data=zipcode, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='zipcode') 
                        zipcode.save()
                        phone_number = Table_data_info(table_id=6, table_col_id=5, user_id=event_contact_user_id, column_data=phone_number, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='phone_number') 
                        phone_number.save()
                        event_first_name = Table_data_info(table_id=5, table_col_id=1, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=first_name, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='first_name') 
                        event_first_name.save()
                        event_last_name = Table_data_info(table_id=5, table_col_id=2, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=last_name, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='last_name') 
                        event_last_name.save()
                        event_email = Table_data_info(table_id=5, table_col_id=3, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=email, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='email') 
                        event_email.save()
                        event_zipcode = Table_data_info(table_id=5, table_col_id=4, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=zipcode, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='zipcode') 
                        event_zipcode.save()
                        event_phone_number = Table_data_info(table_id=5, table_col_id=5, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=phone_number, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='phone_number') 
                        event_phone_number.save()
                        event_check_box = Table_data_info(table_id=5, table_col_id=6, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data="True", table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='check_box') 
                        event_check_box.save()
                    else:
                        first_name = Table_data_info(table_id=6, table_col_id=1, user_id=event_contact_user_id, column_data=first_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='first_name') 
                        first_name.save()
                        last_name = Table_data_info(table_id=6, table_col_id=2, user_id=event_contact_user_id, column_data=last_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='last_name') 
                        last_name.save()
                        email = Table_data_info(table_id=6, table_col_id=3, user_id=event_contact_user_id, column_data=email, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='email') 
                        email.save()
                        zipcode = Table_data_info(table_id=6, table_col_id=4, user_id=event_contact_user_id, column_data=zipcode, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='zipcode') 
                        zipcode.save()
                        phone_number = Table_data_info(table_id=6, table_col_id=5, user_id=event_contact_user_id, column_data=phone_number, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='phone_number') 
                        phone_number.save()
                        event_first_name = Table_data_info(table_id=5, table_col_id=1, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=first_name, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='first_name') 
                        event_first_name.save()
                        event_last_name = Table_data_info(table_id=5, table_col_id=2, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=last_name, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='last_name') 
                        event_last_name.save()
                        event_email = Table_data_info(table_id=5, table_col_id=3, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=email, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='email') 
                        event_email.save()
                        event_zipcode = Table_data_info(table_id=5, table_col_id=4, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=zipcode, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='zipcode') 
                        event_zipcode.save()
                        event_phone_number = Table_data_info(table_id=5, table_col_id=5, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data=phone_number, table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='phone_number') 
                        event_phone_number.save()
                        event_check_box = Table_data_info(table_id=5, table_col_id=6, user_id=event_contact_user_id, tab_rel_id=event_title_detail.table_data_id, column_data="True", table_ref_id=table_ref_id_count_event+1, col_data_type="String", column_name='check_box') 
                        event_check_box.save()
        
           
        return AddContact(first_name=first_name, last_name=last_name, email=email, zipcode=zipcode, phone_number=phone_number, event_first_name=event_first_name, event_last_name=event_last_name, event_email=event_email, event_zipcode=event_zipcode, event_phone_number=event_phone_number, event_check_box=event_check_box)
        


class CreateAddContact(graphene.Mutation):
    first_name = graphene.Field(TableDataInfoType)
    last_name = graphene.Field(TableDataInfoType)
    email = graphene.Field(TableDataInfoType)
    zipcode = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    
    
    # message = graphene.Field(Message)
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        zipcode = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        event_contact_user_id = graphene.String(required=True)
        
    def mutate(self, info, first_name, last_name, email, zipcode, phone_number, event_contact_user_id):
        APICALLFUNCTION('CreateAddContact mutation', 'null')
        
        table_ref_id_count = Table_data_info.objects.filter(table_id=6).count()
        if Table_data_info.objects.filter(column_data=email, table_id=6, user_id=event_contact_user_id).exists():
            raise Exception("Email already exists User Contact.")
        if Table_data_info.objects.filter(column_data=phone_number, table_id=6, user_id=event_contact_user_id).exists():
            raise Exception("Phone Number already exists User Contact.")
        
        first_name = Table_data_info(table_id=6, table_col_id=1, user_id=event_contact_user_id, column_data=first_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='first_name') 
        first_name.save()
        last_name = Table_data_info(table_id=6, table_col_id=2, user_id=event_contact_user_id, column_data=last_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='last_name') 
        last_name.save()
        email = Table_data_info(table_id=6, table_col_id=3, user_id=event_contact_user_id, column_data=email, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='email') 
        email.save()
        zipcode = Table_data_info(table_id=6, table_col_id=4, user_id=event_contact_user_id, column_data=zipcode, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='zipcode') 
        zipcode.save()
        phone_number = Table_data_info(table_id=6, table_col_id=5, user_id=event_contact_user_id, column_data=phone_number, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='phone_number') 
        phone_number.save()
        
    
        return CreateAddContact(first_name=first_name, last_name=last_name, email=email, zipcode=zipcode, phone_number=phone_number) 
        
        
        
class CreateAddDeviceContact(graphene.Mutation):
    first_name = graphene.Field(TableDataInfoType)
    last_name = graphene.Field(TableDataInfoType)
    email = graphene.Field(TableDataInfoType)
    zipcode = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    
    
    class Arguments:
        user_id = graphene.String(required=True)
        
    def mutate(self, info, user_id):
        
        APICALLFUNCTION('CreateAddDeviceContact mutation', 'null')

        userDeviceContact = Table_data_info.objects.filter(table_id=17, user_id=user_id)
        table_ref_id_count = Table_data_info.objects.filter(table_id=6).count()
        if userDeviceContact:
            counti = 1
            device_contact_ref=0
            for i in userDeviceContact: 
                
                if i.column_data!="" and i.column_name == "email":
                    if Table_data_info.objects.filter(column_data=i.column_data, table_id=6, user_id=user_id).exists():
                        raise Exception("Email already exists User Contact.")
                if i.column_data!="" and i.column_name == "phone_number":        
                    if Table_data_info.objects.filter(column_data=i.column_data, table_id=6, user_id=user_id).exists():
                        raise Exception("Mobile already exists User Contact.")
                device_contact_ref += 1
                if device_contact_ref==4:
                    userDeviceContactDetail = Table_data_info.objects.filter(table_id=17, table_ref_id=i.table_ref_id, user_id=user_id)
                    for j in userDeviceContactDetail:
                        if j.column_name == "first_name" and j.table_ref_id==i.table_ref_id:
                            first_name = Table_data_info(table_id=6, table_col_id=1, user_id=user_id, column_data=j.column_data, table_ref_id=table_ref_id_count+counti, col_data_type="String", column_name='first_name') 
                            first_name.save()
                        if j.column_name == "last_name" and j.table_ref_id==i.table_ref_id:
                            last_name = Table_data_info(table_id=6, table_col_id=2, user_id=user_id, column_data=j.column_data, table_ref_id=table_ref_id_count+counti, col_data_type="String", column_name='last_name') 
                            last_name.save()
                        if j.column_name == "email" and j.table_ref_id==i.table_ref_id:
                            email = Table_data_info(table_id=6, table_col_id=3, user_id=user_id, column_data=j.column_data, table_ref_id=table_ref_id_count+counti, col_data_type="String", column_name='email') 
                            email.save()
                        if j.column_name == "phone_number" and j.table_ref_id==i.table_ref_id:
                            zipcode = Table_data_info(table_id=6, table_col_id=4, user_id=user_id, column_data="0", table_ref_id=table_ref_id_count+counti, col_data_type="String", column_name='zipcode') 
                            zipcode.save()
                            phone_number = Table_data_info(table_id=6, table_col_id=5, user_id=user_id, column_data=j.column_data, table_ref_id=table_ref_id_count+counti, col_data_type="String", column_name='phone_number') 
                            phone_number.save()
                            counti = counti + 5
                            device_contact_ref=0
                    

            return CreateAddDeviceContact(first_name=first_name, last_name=last_name, email=email, zipcode=zipcode, phone_number=phone_number)  
            
            
            
            
class EditContact(graphene.Mutation):
    first_name = graphene.Field(TableDataInfoType)
    last_name = graphene.Field(TableDataInfoType)
    email = graphene.Field(TableDataInfoType)
    zipcode = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    
    
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        zipcode = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        user_id = graphene.String(required=True)
        table_id = graphene.Int(required=True)
        table_ref_id = graphene.Int(required=True)
        
    def mutate(self, info, first_name, last_name, email, zipcode, phone_number, user_id, table_id, table_ref_id):
        
        APICALLFUNCTION('EditContact mutation', 'null')
        
        # if Table_data_info.objects.filter(column_data=email, table_id=6, user_id=user_id).exists():
        #     raise Exception("Email already exists User Contact.")
        # if Table_data_info.objects.filter(column_data=phone_number, table_id=6, user_id=user_id).exists():
        #     raise Exception("Phone Number already exists User Contact.")

        editContact = Table_data_info.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id)

        for i in editContact:

            if i.column_name == 'first_name' and i.table_col_id==1:
                first_name1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                first_name1.column_data=first_name
                first_name1.save()
            if i.column_name == 'last_name' and i.table_col_id==2:
                last_name1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                last_name1.column_data=last_name
                last_name1.save()
            if i.column_name == 'email' and i.table_col_id==3:
                email1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                email1.column_data=email
                email1.save()
            if i.column_name == 'zipcode' and i.table_col_id==4:
                zipcode1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                zipcode1.column_data=zipcode
                zipcode1.save()
            if i.column_name == 'phone_number' and i.table_col_id==5:
                phone_number1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                phone_number1.column_data=phone_number
                phone_number1.save()

            
        return EditContact(first_name=first_name1, last_name=last_name1, email=email1, zipcode=zipcode1, phone_number=phone_number1) 
        
        
        
class DeleteContact(graphene.Mutation):
    message = graphene.String()
    
    class Arguments:
        user_id = graphene.String(required=True)
        table_id = graphene.Int(required=True)
        table_ref_id = graphene.Int(required=True)
        
    def mutate(self, info, user_id, table_id, table_ref_id):
        APICALLFUNCTION('DeleteContact mutation', 'null')

        deleteContact = Table_data_info.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id)

        for i in deleteContact:

            if i.column_name == 'first_name' and i.table_col_id==1:
                first_name1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                first_name = Table_data_info.objects.get(table_data_id=first_name1.table_data_id)
                first_name.delete()
            if i.column_name == 'last_name' and i.table_col_id==2:
                last_name1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                last_name = Table_data_info.objects.get(table_data_id=last_name1.table_data_id)
                last_name.delete()
            if i.column_name == 'email' and i.table_col_id==3:
                email1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                email = Table_data_info.objects.get(table_data_id=email1.table_data_id)
                email.delete()
            if i.column_name == 'zipcode' and i.table_col_id==4:
                zipcode1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                zipcode = Table_data_info.objects.get(table_data_id=zipcode1.table_data_id)
                zipcode.delete()
            if i.column_name == 'phone_number' and i.table_col_id==5:
                phone_number1 = Table_data_info.objects.get(table_id=table_id, table_col_id=i.table_col_id, table_ref_id=i.table_ref_id, user_id=i.user_id, column_data=i.column_data, column_name=i.column_name)
                phone_number = Table_data_info.objects.get(table_data_id=phone_number1.table_data_id)
                phone_number.delete()

            
        return DeleteContact(message=f"Contact deleted successfully")        
            


        
class GetContact(graphene.Mutation):
    get_contact = graphene.List(TableDataInfoType)
    
    class Arguments:
        event_contact_user_id = graphene.String(required=True)
        
    def mutate(self, info, event_contact_user_id):
        APICALLFUNCTION('GetContact mutation', 'null')
        # get_contact = Table_data_info.objects.filter(table_id=14).filter(column_data=event_contact_user_id)
        get_contact = Table_data_info.objects.filter(table_id=23)
        print("1530", get_contact)
        return GetContact(get_contact=get_contact)    
        
        
        
        
class AllGuest(graphene.Mutation): 
    message = graphene.String()
    class Arguments:
        table_id = graphene.Int(required=True)
        table_ref_id = graphene.Int(required=True)
        check_box = graphene.String(required=True)
        
    def mutate(self, info, table_id, table_ref_id, check_box):
        APICALLFUNCTION('AllGuest mutation', 'null')
        
        check_box_detail = Table_data_info.objects.get(table_id=table_id, table_ref_id=table_ref_id, column_data=check_box)
       
           
        print('1596', check_box_detail)
        print('1597', check_box_detail.column_data)
        
        if check_box_detail.column_data == "True":
            check_box_detail.column_data = "False"
            check_box_detail.save()
            return AllGuest(message=f"Guest False Successfully")
            
        if check_box_detail.column_data == "False":
            check_box_detail.column_data = "False"
            check_box_detail.save()
            return AllGuest(message=f"Guest False Successfully")
   
            
            
        
        
class SendMessage(graphene.Mutation):
    event_title = graphene.Field(TableDataInfoType)
    date_time = graphene.Field(TableDataInfoType)
    message = graphene.Field(TableDataInfoType)
 
    
    class Arguments:
        message = graphene.String(required=True)
        event_message_user_id = graphene.String(required=True)
        event_title = graphene.String(required=True)
        start_date_and_time = graphene.String(required=True)
        location = graphene.String(required=True)
        hosted_by = graphene.String(required=True)
        bbt = graphene.String(required=True)
        
        
        
    def mutate(self, info, message, event_message_user_id, event_title, start_date_and_time, location, hosted_by, bbt):
        
        APICALLFUNCTION('SendMessage mutation', 'null')
        
        table_ref_id_count = Table_data_info.objects.filter(table_id=7).count()
        print("123", table_ref_id_count+1)
        
        AddContactEventTitle1 = Table_data_info.objects.filter(table_id=4, user_id=event_message_user_id, column_data=event_title)
        if AddContactEventTitle1:
            for m in AddContactEventTitle1:
                if Table_data_info.objects.filter(table_id=4,  user_id=event_message_user_id, column_data=bbt, table_ref_id=m.table_ref_id).exists():
                    AddContactEventTitle = Table_data_info.objects.get(table_id=4, user_id=event_message_user_id, column_data=event_title, table_ref_id=m.table_ref_id)
        
                    AddContact = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, tab_rel_id=AddContactEventTitle.table_data_id)
                    print("1811", AddContact)
                    for j in AddContact:
                        if j.column_name=='email':
                            print("1814", j.column_data)
                            Name_Detail = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, table_ref_id=j.table_ref_id)
                            for k in Name_Detail: 
                                if k.table_col_id==1:
                                    CheckBox_Detail = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, table_ref_id=j.table_ref_id)
                                    for l in CheckBox_Detail: 
                                        if l.column_name=='check_box' and l.column_data=='True':
                                            print("1569", k.column_data)
                                            send_event_message_mail(j.column_data, k.column_data, message, event_title, start_date_and_time,  location, hosted_by)
                        if j.column_name=='phone_number':
                            Name_Detail = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, table_ref_id=j.table_ref_id)
                            for k in Name_Detail: 
                                if k.table_col_id==1:
                                    CheckBox_Detail = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, table_ref_id=j.table_ref_id)
                                    for l in CheckBox_Detail: 
                                        if l.column_name=='check_box' and l.column_data=='True':
                                            print("1569", k.column_data)
                                            sms_send_event(j.column_data, k.column_data, message, event_title, start_date_and_time,  location, hosted_by)
                
        event_title = Table_data_info(table_id=7, table_col_id=1, user_id=event_message_user_id, column_data=event_title, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='event_title') 
        event_title.save()
        date_time = Table_data_info(table_id=7, table_col_id=2, user_id=event_message_user_id, column_data=start_date_and_time, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='date_time') 
        date_time.save()
        message = Table_data_info(table_id=7, table_col_id=3, user_id=event_message_user_id, column_data=message, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='message') 
        message.save()
        
        
        return SendMessage(message=message, event_title=event_title, date_time=date_time)     
        
        
        
class ContactSendMessage(graphene.Mutation):
    event_title = graphene.Field(TableDataInfoType)
    date_time = graphene.Field(TableDataInfoType)
    message = graphene.Field(TableDataInfoType)
 
    
    class Arguments:
        message = graphene.String(required=True)
        event_message_user_id = graphene.String(required=True)
        event_title = graphene.String(required=True)
        start_date_and_time = graphene.String(required=True)
        location = graphene.String(required=True)
        tabledataid = graphene.Int(required=True)
        hosted_by = graphene.String(required=True)
        
        
    def mutate(self, info, message, event_message_user_id, event_title, start_date_and_time, location, tabledataid, hosted_by):
        
        APICALLFUNCTION('ContactSendMessage mutation', 'null')

        
        table_ref_id_count = Table_data_info.objects.filter(table_id=7).count()
        print("123", table_ref_id_count+1)
        
        AddContactEventTitle1 = Table_data_info.objects.filter(table_id=4, user_id=event_message_user_id, column_data=event_title)
        if AddContactEventTitle1:
            for m in AddContactEventTitle1:
                if Table_data_info.objects.filter(table_id=4,  user_id=event_message_user_id, column_data=bbt, table_ref_id=m.table_ref_id).exists():
                    AddContactEventTitle = Table_data_info.objects.get(table_id=4, user_id=event_message_user_id, column_data=event_title, table_ref_id=m.table_ref_id)
                    AddContact = Table_data_info.objects.filter(table_id=5, user_id=event_message_user_id, tab_rel_id=AddContactEventTitle.table_data_id)
                    print("1811", AddContact)
                    for j in AddContact:
                        if j.table_col_id==3:
                            print("1814", j.column_data)
                            CheckBox_Detail = Table_data_info.objects.filter(table_id=5, table_ref_id=j.table_ref_id)
                            for k in CheckBox_Detail: 
                                if k.table_col_id==1:
                                    print("1569", k.column_data)
                                    send_contact_message_mail(j.column_data, k.column_data, message, event_title, start_date_and_time, location, tabledataid, hosted_by)
                        if j.table_col_id==5:
                            print("1516", j.column_data)
                            CheckBox_Detail1 = Table_data_info.objects.filter(table_id=5, table_ref_id=j.table_ref_id)
                            for k in CheckBox_Detail1: 
                                if k.table_col_id==1:
                                    print("1569", k.column_data)
                                    sms_send_contact(j.column_data, k.column_data, message, event_title, start_date_and_time, location, tabledataid, hosted_by)
                
        event_title = Table_data_info(table_id=7, table_col_id=1, user_id=event_message_user_id, column_data=event_title, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='event_title') 
        event_title.save()
        date_time = Table_data_info(table_id=7, table_col_id=2, user_id=event_message_user_id, column_data=start_date_and_time, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='date_time') 
        date_time.save()
        message = Table_data_info(table_id=7, table_col_id=3, user_id=event_message_user_id, column_data=message, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='message') 
        message.save()
        
        
        return ContactSendMessage(message=message, event_title=event_title, date_time=date_time)    
        
        
        
class LogMutationApp(graphene.Mutation):
    result = graphene.Boolean(required=True)
 
    
    class Arguments:
        log_event = graphene.String(required=True)
        
        
    def mutate(self, info, log_event):
        APICALLFUNCTION('LogMutationApp mutation', 'null')
        
        time = str(CurrentTimeStand())
        
        AppJsonLogFile(log_event, time)
        
        return LogMutationApp(result=True)
        
        
        
class UserDeviceInfoMutation(graphene.Mutation):
    Userid = graphene.Field(TableDataInfoType)
    Macid = graphene.Field(TableDataInfoType)
    Mobile_brand_name = graphene.Field(TableDataInfoType)
    Mac_user_id = graphene.Field(TableDataInfoType)
    Android_user_id = graphene.Field(TableDataInfoType)
    Os_version = graphene.Field(TableDataInfoType)
    ip_address = graphene.Field(TableDataInfoType)
    result = graphene.Boolean()
    
    
    class Arguments:
        Userid = graphene.String(required=True)
        Macid = graphene.String(required=True)
        Mobile_brand_name = graphene.String(required=True)
        Mac_user_id = graphene.String()
        Android_user_id = graphene.String()
        Os_version = graphene.String(required=True)
        ip_address = graphene.String(required=True)
        
    def mutate(self, info, Userid, Macid, Mobile_brand_name, Mac_user_id, Android_user_id, Os_version, ip_address):
        
        APICALLFUNCTION('UserDeviceInfoMutation mutation', 'null')

        

        table_ref_id_count = Table_data_info.objects.filter(table_id=15).count()
        if Table_data_info.objects.filter(column_data=Macid, table_id=15, user_id=Userid).exists():
            if Table_data_info.objects.filter(column_data=Mobile_brand_name, table_id=15, user_id=Userid).exists():
                return UserDeviceInfoMutation(result=True)
        
        Userid = Table_data_info(table_id=15, table_col_id=1, user_id=Userid, column_data=Userid, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Userid') 
        Userid.save()
        Macid = Table_data_info(table_id=15, table_col_id=2, user_id=Userid, column_data=Macid, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Macid') 
        Macid.save()
        Mobile_brand_name = Table_data_info(table_id=15, table_col_id=3, user_id=Userid, column_data=Mobile_brand_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Mobile_brand_name') 
        Mobile_brand_name.save()
        Mac_user_id = Table_data_info(table_id=15, table_col_id=4, user_id=Userid, column_data=Mac_user_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Mac_user_id') 
        Mac_user_id.save()
        Android_user_id = Table_data_info(table_id=15, table_col_id=5, user_id=Userid, column_data=Android_user_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Android_user_id') 
        Android_user_id.save()
        Os_version = Table_data_info(table_id=15, table_col_id=6, user_id=Userid, column_data=Os_version, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='Os_version') 
        Os_version.save()
        ip_address = Table_data_info(table_id=15, table_col_id=7, user_id=Userid, column_data=ip_address, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='ip_address') 
        ip_address.save()

    
    
        return UserDeviceInfoMutation(Userid=Userid, Macid=Macid, Mobile_brand_name=Mobile_brand_name, Mac_user_id=Mac_user_id, Android_user_id=Android_user_id, Os_version=Os_version, ip_address=ip_address)        
        
        
class DeviceContactsMutation(graphene.Mutation):
    first_name = graphene.Field(TableDataInfoType)
    last_name = graphene.Field(TableDataInfoType)
    email = graphene.Field(TableDataInfoType)
    phone_number = graphene.Field(TableDataInfoType)
    
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone_number = graphene.String(required=True)
        user_id = graphene.String(required=True)
        
    def mutate(self, info, first_name, last_name, email, phone_number, user_id):
        
        APICALLFUNCTION('DeviceContactsMutation mutation', 'null')

        table_ref_id_count = Table_data_info.objects.filter(table_id=17).count()
        
        if email!="":
            if Table_data_info.objects.filter(column_data=email, table_id=17, user_id=user_id).exists():
                raise Exception("Email already exists Device Contact.")
            if Table_data_info.objects.filter(column_data=email, table_id=6, user_id=user_id).exists():
                raise Exception("Email already exists User Contact.")
        if Table_data_info.objects.filter(column_data=phone_number, table_id=17, user_id=user_id).exists():
            raise Exception("Phone Number already exists Device Contact.")
        if Table_data_info.objects.filter(column_data=phone_number, table_id=6, user_id=user_id).exists():
            raise Exception("Phone Number already exists User Contact.")
            
        if len(phone_number)>=10:
            first_name = Table_data_info(table_id=17, table_col_id=1, user_id=user_id, column_data=first_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='first_name') 
            first_name.save()
            last_name = Table_data_info(table_id=17, table_col_id=2, user_id=user_id, column_data=last_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='last_name') 
            last_name.save()
            email = Table_data_info(table_id=17, table_col_id=3, user_id=user_id, column_data=email, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='email') 
            email.save()
            phone_number = Table_data_info(table_id=17, table_col_id=4, user_id=user_id, column_data=phone_number, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='phone_number') 
            phone_number.save()
            
            return DeviceContactsMutation(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        
        
        
class ForgetPasswordSendEmailMutation(graphene.Mutation):
    message = graphene.String(required=True)

    class Arguments:
        email = graphene.String(required=True)
        
        
    def mutate(self, info, email):
        
        APICALLFUNCTION('ForgetPasswordSendEmailMutation mutation', 'null')
        
        if not Table_data_info.objects.filter(column_data=email, table_id=1).first():
            raise Exception("Email is not valid")
        user = Table_data_info.objects.get(column_data=email, table_id=1)

        flag = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
        for i in flag:
            if i.table_col_id==6 and i.column_name=="is_email_verified" and i.column_data=="True":
                flag1 = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
                for j in flag1:
                    if j.table_col_id==4 and j.column_name=="is_active" and j.column_data=="True":
                        send_forget_password_email(email)
                        return ForgetPasswordSendEmailMutation(message=f"Send Email Successfully.")   
                        
                        
class ChangePasswordSendEmailMutation(graphene.Mutation):
    message = graphene.String(required=True)

    class Arguments:
        email = graphene.String(required=True)
        
        
    def mutate(self, info, email):
        
        APICALLFUNCTION('ChangePasswordSendEmailMutation mutation', 'null')
        
        if not Table_data_info.objects.filter(column_data=email, table_id=1).first():
            raise Exception("Email is not valid")
        user = Table_data_info.objects.get(column_data=email, table_id=1)

        flag = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
        for i in flag:
            if i.table_col_id==6 and i.column_name=="is_email_verified" and i.column_data=="True":
                flag1 = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
                for j in flag1:
                    if j.table_col_id==4 and j.column_name=="is_active" and j.column_data=="True":
                        send_change_password_email(email)
                        return ChangePasswordSendEmailMutation(message=f"Send Email Successfully.")
                        
    
    
class UserCourseMcqAns(graphene.Mutation):
    course_id = graphene.Field(TableDataInfoType)
    chapter_id = graphene.Field(TableDataInfoType)
    question_id = graphene.Field(TableDataInfoType)
    mcq_option_no = graphene.Field(TableDataInfoType)
    result = graphene.Field(TableDataInfoType)
    message = graphene.String()
    
    
    class Arguments:
        course_id = graphene.String(required=True)
        chapter_id = graphene.String(required=True)
        question_id = graphene.String(required=True)
        mcq_option_no = graphene.String(required=True)
        result = graphene.String(required=True)
        user_id = graphene.String(required=True)
        count_of_chapter = graphene.Int(required=True)
        count_of_true = graphene.Int(required=True)
        next_chapter_id = graphene.String(required=True)
        
    def mutate(self, info, course_id, chapter_id, question_id, mcq_option_no, result, user_id, count_of_chapter, count_of_true, next_chapter_id):
        
        APICALLFUNCTION('UserCourseMcqAns mutation', 'null')

        question_d = Table_data_info.objects.filter(table_id=23, table_col_id=3, user_id=user_id, column_data=question_id)
        
        if question_d.count() == 0:
            chapter_d = Table_data_info.objects.filter(table_id=23, table_col_id=2, user_id=user_id, column_data=chapter_id)
            if chapter_d.count() == 0:
                course_d = Table_data_info.objects.filter(table_id=25, table_col_id=2, user_id=user_id, column_data=course_id)
                for i in course_d:
                    course_reg = Table_data_info.objects.filter(table_id=25, user_id=user_id, table_ref_id=i.table_ref_id)
                    for j in course_reg:
                        if j.table_col_id==8 and j.column_name=='course_complete_percent' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                            course_complete_percent = Table_data_info.objects.get(table_id=25, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                            course_complete_percent.column_data = int((count_of_true*100)/count_of_chapter)
                            course_complete_percent.save()
            
            
            table_ref_id_count = Table_data_info.objects.all().last()
            
            course_id = Table_data_info(table_id=23, table_col_id=1, user_id=user_id, column_data=course_id, table_ref_id=table_ref_id_count.table_data_id+23, col_data_type="String", column_name='course_id') 
            course_id.save()
            chapter_id = Table_data_info(table_id=23, table_col_id=2, user_id=user_id, column_data=chapter_id, table_ref_id=table_ref_id_count.table_data_id+23, col_data_type="String", column_name='chapter_id') 
            chapter_id.save()
            question_id = Table_data_info(table_id=23, table_col_id=3, user_id=user_id, column_data=question_id, table_ref_id=table_ref_id_count.table_data_id+23, col_data_type="String", column_name='question_id') 
            question_id.save()
            mcq_option_no = Table_data_info(table_id=23, table_col_id=4, user_id=user_id, column_data=mcq_option_no, table_ref_id=table_ref_id_count.table_data_id+23, col_data_type="String", column_name='mcq_option_no') 
            mcq_option_no.save()
            result = Table_data_info(table_id=23, table_col_id=5, user_id=user_id, column_data=result, table_ref_id=table_ref_id_count.table_data_id+23, col_data_type="String", column_name='result') 
            result.save()
            
            if next_chapter_id:
                flag_d = Table_data_info.objects.filter(table_id=27, table_col_id=3, user_id=user_id, column_data=next_chapter_id)
                if flag_d:
                    for i in flag_d:
                        flag_d1 = Table_data_info.objects.filter(table_id=27, user_id=user_id, table_ref_id=i.table_ref_id)
                        for j in flag_d1:
                            if j.table_col_id==4 and j.column_name=='flag' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                                flag_update = Table_data_info.objects.get(table_id=27, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                                flag_update.column_data = "true"
                                flag_update.save()


            return UserCourseMcqAns(course_id=course_id, chapter_id=chapter_id, question_id=question_id, mcq_option_no=mcq_option_no, result=result)

        else:
            question_d = Table_data_info.objects.get(table_id=23, table_col_id=3, user_id=user_id, column_data=question_id)
            total_mcq_ans = Table_data_info.objects.filter(table_id=23, user_id=user_id, table_ref_id=question_d.table_ref_id)
            for j in total_mcq_ans:
                if j.table_col_id==4 and j.column_name=='mcq_option_no' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                    mcq_option = Table_data_info.objects.get(table_id=23, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                    mcq_option.column_data = mcq_option_no
                    mcq_option.save()
                if j.table_col_id==5 and j.column_name=='result' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                    mcq_result = Table_data_info.objects.get(table_id=23, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                    mcq_result.column_data = result
                    mcq_result.save()
            return UserCourseMcqAns(message="mcq updated")
            
            
class ExamUserCourseMcqAns(graphene.Mutation):
    course_id = graphene.Field(TableDataInfoType)
    chapter_id = graphene.Field(TableDataInfoType)
    question_id = graphene.Field(TableDataInfoType)
    mcq_option_no = graphene.Field(TableDataInfoType)
    result = graphene.Field(TableDataInfoType)
    message = graphene.String()
    
    
    class Arguments:
        course_id = graphene.String(required=True)
        chapter_id = graphene.String(required=True)
        question_id = graphene.String(required=True)
        mcq_option_no = graphene.String(required=True)
        result = graphene.String(required=True)
        user_id = graphene.String(required=True)
       
        
    def mutate(self, info, course_id, chapter_id, question_id, mcq_option_no, result, user_id):
        APICALLFUNCTION('ExamUserCourseMcqAns mutation', 'null')
        question_d = Table_data_info.objects.filter(table_id=533, table_col_id=3, user_id=user_id, column_data=question_id)
        if question_d.count() == 0:
            table_ref_id_count = Table_data_info.objects.all().last()
            course_id = Table_data_info(table_id=533, table_col_id=1, user_id=user_id, column_data=course_id, table_ref_id=table_ref_id_count.table_data_id+533, col_data_type="String", column_name='course_id') 
            course_id.save()
            chapter_id = Table_data_info(table_id=533, table_col_id=2, user_id=user_id, column_data=chapter_id, table_ref_id=table_ref_id_count.table_data_id+533, col_data_type="String", column_name='chapter_id') 
            chapter_id.save()
            question_id = Table_data_info(table_id=533, table_col_id=3, user_id=user_id, column_data=question_id, table_ref_id=table_ref_id_count.table_data_id+533, col_data_type="String", column_name='question_id') 
            question_id.save()
            mcq_option_no = Table_data_info(table_id=533, table_col_id=4, user_id=user_id, column_data=mcq_option_no, table_ref_id=table_ref_id_count.table_data_id+533, col_data_type="String", column_name='mcq_option_no') 
            mcq_option_no.save()
            result = Table_data_info(table_id=533, table_col_id=5, user_id=user_id, column_data=result, table_ref_id=table_ref_id_count.table_data_id+533, col_data_type="String", column_name='result') 
            result.save()
                

            return ExamUserCourseMcqAns(course_id=course_id, chapter_id=chapter_id, question_id=question_id, mcq_option_no=mcq_option_no, result=result)
            
        else:
            question_d = Table_data_info.objects.get(table_id=533, table_col_id=3, user_id=user_id, column_data=question_id)
            total_mcq_ans = Table_data_info.objects.filter(table_id=533, user_id=user_id, table_ref_id=question_d.table_ref_id)
            for j in total_mcq_ans:
                if j.table_col_id==4 and j.column_name=='mcq_option_no' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                    mcq_option = Table_data_info.objects.get(table_id=533, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                    mcq_option.column_data = mcq_option_no
                    mcq_option.save()
                if j.table_col_id==5 and j.column_name=='result' and j.table_ref_id==j.table_ref_id and j.column_data==j.column_data and j.user_id==user_id:
                    mcq_result = Table_data_info.objects.get(table_id=533, table_col_id=j.table_col_id, column_name=j.column_name, column_data=j.column_data, user_id=j.user_id, table_ref_id=j.table_ref_id)
                    mcq_result.column_data = result
                    mcq_result.save()
            return ExamUserCourseMcqAns(message="result updated")    
        
class UserCourseChapter(graphene.Mutation):
    user_id = graphene.Field(TableDataInfoType)
    course_id = graphene.Field(TableDataInfoType)
    chapter_id = graphene.Field(TableDataInfoType)
    flag = graphene.Field(TableDataInfoType)
    
    
    class Arguments:
        user_id = graphene.String(required=True)
        course_id = graphene.String(required=True)
        chapter_id = graphene.String(required=True)
        flag = graphene.String(required=True)
        
        
    def mutate(self, info, course_id, chapter_id, flag, user_id):
        APICALLFUNCTION('UserCourseChapter mutation', 'null')

        table_ref_id_count = Table_data_info.objects.filter(table_id=27).count()

        chapter_d = Table_data_info.objects.filter(table_id=27, table_col_id=3, user_id=user_id, column_data=chapter_id)
        if chapter_d:
            return
        else:
            user_id = Table_data_info(table_id=27, table_col_id=1, user_id=user_id, column_data=user_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='user_id') 
            user_id.save()
            course_id = Table_data_info(table_id=27, table_col_id=2, user_id=user_id, column_data=course_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='course_id') 
            course_id.save()
            chapter_id = Table_data_info(table_id=27, table_col_id=3, user_id=user_id, column_data=chapter_id, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='chapter_id') 
            chapter_id.save()
            flag = Table_data_info(table_id=27, table_col_id=4, user_id=user_id, column_data=flag, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='flag') 
            flag.save()
            return UserCourseChapter(user_id=user_id, course_id=course_id, chapter_id=chapter_id, flag=flag)
            




from reportlab.lib.pagesizes import LETTER, A4, LEGAL, TABLOID 
from reportlab.lib.units import inch  
from reportlab.pdfgen.canvas import Canvas  
from reportlab.lib.colors import purple, white 

import requests            

def certificatepredineformat(email_name, first_name, last_name, middlename, dob, gender, classroom_completion_date, laboratory_date, ptde_course_number, issue_date, phone_number):
        
        my_certificate = Canvas(f"/home/itbusaah/idriver_education_djangoproject/media/upload_file/certificate/{email_name}.pdf", pagesize = (1914.85, 1278.77)) 
        certificate_image_path = "/home/itbusaah/idriver_education_djangoproject/media/upload_file/certificate/certificateimage.jpg"
        my_certificate.drawImage(certificate_image_path, 40, 40, width=1834.85, height=1198.77, preserveAspectRatio=True, mask='auto')
        my_certificate.setTitle("Certificate")
        #lastname
        if last_name!="":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(165, 815, last_name)

        #firstname
        if first_name != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(550, 815, first_name)

        #middlename
        if middlename != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(890, 815, middlename)

        #dateofbirth
        if dob != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(1205, 815, dob)
        # gender
        if  gender != "":       
                if gender == "Male":
                        #male sign
                        my_certificate.setFillColor("black")  
                        my_certificate.setFont("Times-Bold", 45)    
                        my_certificate.drawString(1515, 810, "✔")
                elif gender == "Female":
                        #female sign
                        my_certificate.setFillColor("black")  
                        my_certificate.setFont("Times-Bold", 45)    
                        my_certificate.drawString(1660, 810, "✔")

        #classroom completion
        if classroom_completion_date != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(895, 740, classroom_completion_date)

        #laboratory completion
        if laboratory_date != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(1575, 740, laboratory_date)

        #signature 
        signature_image_path = "/home/itbusaah/idriver_education_djangoproject/media/upload_file/certificate/signature.png"
        my_certificate.drawImage(signature_image_path, 100, 360, width=350, height=300, preserveAspectRatio=True, mask='auto')


        #ptde course number 
        if ptde_course_number != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(690, 500, "#")
                my_certificate.drawString(715, 500, ptde_course_number)

        #issue date 
        if issue_date != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 45)    
                my_certificate.drawString(1180, 500, issue_date)

        #school phone number 
        if phone_number != "":
                my_certificate.setFillColor("black")  
                my_certificate.setFont("Times-Bold", 35)    
                my_certificate.drawString(1490, 510, phone_number)

        my_certificate.save()    

        
        

class CourseRegistrationPercentage(graphene.Mutation):
    message = graphene.String()
    
    
    class Arguments:
        user_id = graphene.String(required=True)
        course_id = graphene.String(required=True)
        
        
    def mutate(self, info, course_id, user_id):
        
        APICALLFUNCTION('CourseRegistrationPercentage mutation', 'null')

        
        sections = {}
        items = []
        refId = []

        user_sections = {}
        course_reg_sections = {}
        course_sections = {}

        user_data = Table_data_info.objects.filter(table_id=1, user_id=user_id).order_by('table_ref_id')
        if user_data:
            for i in user_data:
                if i.table_col_id==1:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==2:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==3:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==4:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==5:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==6:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==7:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==8:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==9:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==10:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==11:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==12:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==13:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==14:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==15:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==16:
                    user_sections[i.column_name]  = i.column_data
                if i.table_col_id==17:
                    user_sections[i.column_name]  = i.column_data        

        course_registration = Table_data_info.objects.get(table_data_id=course_id)
        course_data = Table_data_info.objects.filter(table_id=18, table_ref_id=course_registration.table_ref_id).order_by('table_ref_id')
        if course_data:
            for c in course_data:
                if c.table_col_id==1:
                    course_sections[c.column_name]  = c.column_data
                if c.table_col_id==2:
                    course_sections[c.column_name]  = c.column_data
                if c.table_col_id==3:
                    course_sections[c.column_name]  = c.column_data
                if c.table_col_id==4:
                    course_sections[c.column_name]  = c.column_data
                if c.table_col_id==5:
                    course_sections[c.column_name]  = c.column_data
                if c.table_col_id==6:
                    course_sections[c.column_name]  = c.column_data
                    
                    
        course_registration_p = Table_data_info.objects.get(table_id=25, user_id=user_id, column_data=course_id)         
            
        course_registration_data = Table_data_info.objects.filter(table_id=25, user_id=course_registration_p.user_id, table_ref_id=course_registration_p.table_ref_id).order_by('table_ref_id')
        if course_registration_data:
            for l in course_registration_data:
                if l.table_col_id==8 and l.column_name=='course_complete_percent' and l.table_ref_id==l.table_ref_id and l.column_data=="100" and l.user_id==user_id:
                    course_complete_date_data = Table_data_info.objects.filter(table_id=25, user_id=l.user_id, table_ref_id=l.table_ref_id).order_by('table_ref_id')
                    for m in course_complete_date_data:
                        if m.table_col_id==6 and m.column_name=='course_complete_flag' and m.table_ref_id==m.table_ref_id and m.user_id==user_id:
                            course_complete_date_update = Table_data_info.objects.get(table_id=25, table_col_id=m.table_col_id, column_name=m.column_name, user_id=m.user_id, table_ref_id=m.table_ref_id)
                            course_complete_date_update.column_data = "true"
                            course_complete_date_update.save()
                            
                        if m.table_col_id==13 and m.column_name=='course_completion_date' and m.table_ref_id==m.table_ref_id and m.user_id==user_id:
                            course_complete_date_update = Table_data_info.objects.get(table_id=25, table_col_id=m.table_col_id, column_name=m.column_name, user_id=m.user_id, table_ref_id=m.table_ref_id)
                            course_complete_date_update.column_data = currenttimedate
                            course_complete_date_update.save()
                            
                            course_reg_objects = Table_data_info.objects.filter(table_id=25, user_id=m.user_id, table_ref_id=m.table_ref_id).order_by('table_ref_id')
                            for z in course_reg_objects:
                                if z.table_col_id==1:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==2:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==3:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==4:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==5:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==6:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==7:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==8:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==9:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==10:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==11:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==12:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==13:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==14:
                                    course_reg_sections[z.column_name]  = z.column_data
                                if z.table_col_id==15:
                                    course_reg_sections[z.column_name]  = z.column_data

                        
                            email_name = user_sections['email'][:user_sections['email'].index('@')]
                            certificatepredineformat(email_name=email_name, first_name=user_sections['first_name'], last_name=user_sections['last_name'], middlename=user_sections['middle_name'], dob=user_sections['dob'], gender=user_sections['gender'], classroom_completion_date=course_reg_sections['course_completion_date'], laboratory_date=course_reg_sections['laboratory_completion_date'], ptde_course_number=course_sections['course_id'], issue_date=course_reg_sections['issue_date'], phone_number=user_sections['phone_number'])
                            return CourseRegistrationPercentage(message="100 Percentage Updated and Pdf Generated Successfully")


        return CourseRegistrationPercentage(message="percentage updated")



class CourseMcqFinalResult(graphene.Mutation):
    result = graphene.Boolean()
    
    class Arguments:
        
        user_id = graphene.String(required=True)
        course_id = graphene.String(required=True)
        
        
    def mutate(self, info, user_id, course_id):
        APICALLFUNCTION('CourseMcqFinalResult mutation', 'null')
        course_data = Table_data_info.objects.get(table_id=25, user_id=user_id, column_data=course_id)
        course_dtl = Table_data_info.objects.filter(table_id=25, user_id=user_id, table_ref_id=course_data.table_ref_id)
        user_mcq_ans_data = Table_data_info.objects.filter(table_id=23, table_col_id=1, user_id=user_id, column_data=course_id)
        course_mcq_true_result_count=0
        for m in user_mcq_ans_data:
            course_mcq_true_result_count += Table_data_info.objects.filter(table_id=23, table_col_id=5, user_id=user_id, table_ref_id=m.table_ref_id, column_data="true").count()
        if course_dtl:
            for i in course_dtl:
                if i.table_col_id == 4:
                    minimum_passing_score = i.column_data
                    for j in course_dtl:
                        if j.table_col_id == 15:
                            percentage_result = ((course_mcq_true_result_count*100)/(int(j.column_data)))
                            if int(minimum_passing_score)<=int(percentage_result):
                                return CourseMcqFinalResult(result=True)
                            
        
        return CourseMcqFinalResult(result=False)
        
        
        
class ExamCourseMcqFinalResult(graphene.Mutation):
    result = graphene.Int()
    
    class Arguments:
        
        user_id = graphene.String(required=True)
        course_id = graphene.String(required=True)
        
        
    def mutate(self, info, user_id, course_id):
        APICALLFUNCTION('ExamCourseMcqFinalResult mutation', 'null')
        course_data = Table_data_info.objects.get(table_id=25, user_id=user_id, column_data=course_id)
        course_dtl = Table_data_info.objects.filter(table_id=25, user_id=user_id, table_ref_id=course_data.table_ref_id)
        user_mcq_ans_data = Table_data_info.objects.filter(table_id=533, table_col_id=1, user_id=user_id, column_data=course_id)
        course_mcq_true_result_count=0
        for m in user_mcq_ans_data:
            course_mcq_true_result_count += Table_data_info.objects.filter(table_id=533, table_col_id=5, user_id=user_id, table_ref_id=m.table_ref_id, column_data="true").count()
        if course_dtl:
            for j in course_dtl:
                if j.table_col_id == 15:
                    percentage_result = ((course_mcq_true_result_count*100)/(int(j.column_data)))
                    return ExamCourseMcqFinalResult(result=int(percentage_result))        
        
        
        
def TableDataFile(table_data_id, table_id, column_id, column_name, column_data):
    def write_json(new_data, filename='/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/TableData.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["table_data"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
    y = {
        "table_data_id": table_data_id,
        "table_id": table_id,
        "column_id": column_id,
        "column_name": column_name,
        "column_data": column_data,
        }
        
    write_json(y) 

class TableDataCreate(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_data_id = graphene.String(required=True)
        table_id = graphene.String(required=True)
        column_id = graphene.String(required=True)
        column_name = graphene.String(required=True)
        column_data = graphene.String(required=True)

    def mutate(self, info, table_data_id, table_id, column_id, column_name, column_data):
        APICALLFUNCTION('TableDataCreate mutation', 'null')
        TableDataFile(table_data_id, table_id, column_id, column_name, column_data)
        return TableDataCreate(message="Table Data Created successfully")  
        
        
        
        
        
        
class CreateTableInfoDetail(graphene.Mutation):
    table_info_dtl = graphene.Field(TableInfoDtlType)
    message = graphene.String()
    
    class Arguments:
        table_name = graphene.String(required=True)
        table_description = graphene.String(required=True)
        table_type = graphene.String(required=True)
        
        
    def mutate(self, info, table_name, table_description, table_type):
        APICALLFUNCTION('CreateTableInfoDetail mutation', 'null')
        table_dtl = Table_info_dtl.objects.filter(table_name=table_name)
        if table_dtl.count() == 0:
            Tableinfodtl = Table_info_dtl(table_name=table_name, table_description=table_description, table_type=table_type) 
            Tableinfodtl.save()    
            return CreateTableInfoDetail(table_info_dtl=Tableinfodtl, message=f"{table_name} Table Created Successfully") 
        else:
             return CreateTableInfoDetail(message=f"{table_name} table name already exists, Please give another table name and try again") 



class UpdateTableInfoDetail(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        old_table_name = graphene.String(required=True)
        new_table_name = graphene.String(required=True)
        table_description = graphene.String(required=True)
        table_type = graphene.String(required=True)

    def mutate(self, info,  old_table_name, new_table_name, table_description, table_type):
        APICALLFUNCTION('UpdateTableInfoDetail mutation', 'null')
        record = Table_info_dtl.objects.filter(table_name=old_table_name)
        if record.count() == 1:
            record1 = Table_info_dtl.objects.get(table_name=old_table_name)
            record1.table_name=new_table_name
            record1.table_description=table_description
            record1.table_type=table_type
            record1.save()
            return UpdateTableInfoDetail(message=f"{old_table_name} table name is successfully updated")
        else: 
            return UpdateTableInfoDetail(message=f"{old_table_name} table name is not found")



class DeleteTableInfoDetail(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_name = graphene.String(required=True)
       

    def mutate(self, info, table_name):
        APICALLFUNCTION('DeleteTableInfoDetail mutation', 'null')
        record = Table_info_dtl.objects.filter(table_name=table_name)
        if record.count() == 1:
            table_dtl = Table_info_dtl.objects.get(table_name=table_name)
            table_col_info = Table_col_info.objects.filter(table_id=table_dtl.table_id)
            table_data_info = Table_data_info.objects.filter(table_id=table_dtl.table_id)
            if table_col_info.count() == 0 and table_data_info.count() == 0:
                table_dtl.delete()
                return DeleteTableInfoDetail(message=f"{table_name} table name is successfully deleted")
            else:
                 return DeleteTableInfoDetail(message=f"{table_name} table name of  table_col_info or table_data_info any value exists in your database.So I can't delete the {table_name} table name")
        else:
            return DeleteTableInfoDetail(message=f"{table_name} table name is not found") 
        
        
        
class CreateTableColInfo(graphene.Mutation):
    table_col_info = graphene.Field(TableColInfoType)
    message = graphene.String()
    
    class Arguments:
        table_name = graphene.String(required=True)
        table_col_id = graphene.Int(required=True)
        column_name = graphene.String(required=True)
        col_data_type = graphene.String(required=True)
        col_desc = graphene.String(required=True)
        col_classi = graphene.String(required=True)
        
        
    def mutate(self, info, table_name, table_col_id, column_name, col_data_type, col_desc, col_classi):
        APICALLFUNCTION('CreateTableColInfo mutation', 'null')
        table_dtl = Table_info_dtl.objects.filter(table_name=table_name)
        if table_dtl.count() == 1:
            table_dtl1 = Table_info_dtl.objects.get(table_name=table_name)
            Tablecolinfo = Table_col_info(table_id=table_dtl1.table_id, table_col_id=table_col_id, column_name=column_name, col_data_type=col_data_type, col_desc=col_desc, col_classi=col_classi) 
            Tablecolinfo.save()    
            return CreateTableColInfo(table_col_info=Tablecolinfo, message=f"{table_name} table name of column created successfully") 
        else:
            return CreateTableColInfo(message=f"{table_name} table name is not found")
        
class UpdateTableColInfo(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_name = graphene.String(required=True)
        table_col_id = graphene.Int(required=True)
        old_column_name = graphene.String(required=True)
        new_column_name = graphene.String(required=True)
        col_data_type = graphene.String(required=True)
        col_desc = graphene.String(required=True)
        col_classi = graphene.String(required=True)

    def mutate(self, info, table_name, table_col_id, old_column_name, new_column_name, col_data_type, col_desc, col_classi):
        APICALLFUNCTION('UpdateTableColInfo mutation', 'null')
        table_dtl = Table_info_dtl.objects.filter(table_name=table_name)
        if table_dtl.count() == 1:
            table_dtl1 = Table_info_dtl.objects.get(table_name=table_name)
            record = Table_col_info.objects.filter(table_id=table_dtl1.table_id, column_name=old_column_name)
            if record.count() == 1:
                record1 = Table_col_info.objects.get(table_id=table_dtl1.table_id, column_name=old_column_name)
                record1.table_col_id=table_col_id
                record1.column_name=new_column_name
                record1.col_data_type=col_data_type
                record1.col_desc=col_desc
                record1.col_classi=col_classi
                record1.save()
                return UpdateTableColInfo(message=f"{table_name} table name of  {old_column_name} column name is successfully updated") 
            else:
                return UpdateTableColInfo(message=f"{table_name} table name of  {old_column_name} column name is not found")
        else:
            return UpdateTableColInfo(message=f"{table_name} table name is not found")

class DeleteTableColInfo(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_name = graphene.String(required=True)
        column_name = graphene.String(required=True)
       

    def mutate(self, info, table_name, column_name):
        APICALLFUNCTION('DeleteTableColInfo mutation', 'null')
        table_dtl = Table_info_dtl.objects.filter(table_name=table_name)
        if table_dtl.count() == 1:
            table_dtl1 = Table_info_dtl.objects.get(table_name=table_name)
            record = Table_col_info.objects.filter(table_id=table_dtl1.table_id, column_name=column_name)
            if record.count() == 1:
                record1 = Table_col_info.objects.get(table_id=table_dtl1.table_id, column_name=column_name)
                record1.delete()
                return DeleteTableColInfo(message=f"{table_name} table name of {column_name} column is successfully deleted")                                
            else:
                return DeleteTableColInfo(message=f"{table_name} table name of {column_name} column is not found")
        else:
            return DeleteTableColInfo(message=f"{table_name} table name is not found")
        
        

class DeleteTableRowWithTableRefId(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_id = graphene.Int(required=True)
        table_ref_id = graphene.String(required=True)
       

    def mutate(self, info, table_id, table_ref_id):
        APICALLFUNCTION('DeleteTableRowWithTableRefId mutation', 'null')
        record = Table_data_info.objects.filter(table_id=table_id, table_ref_id=table_ref_id)
        if record:
            for i in record:
                table_data = Table_data_info.objects.get(table_data_id=i.table_data_id)
                table_data.delete()
            return DeleteTableRowWithTableRefId(message=f"{table_id} table_id and {table_ref_id} table_ref_id data deleted successfully")
        else:
            return DeleteTableRowWithTableRefId(message=f"{table_id} table_id and {table_ref_id} table_ref_id data is not found")
            
            
            
class DeleteTableRowWithTableRelId(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_id = graphene.Int(required=True)
        table_rel_id = graphene.String(required=True)
       

    def mutate(self, info, table_id, table_rel_id):
        APICALLFUNCTION('DeleteTableRowWithTableRelId mutation', 'null')
        record = Table_data_info.objects.filter(table_id=table_id, tab_rel_id=table_rel_id)
        if record:
            for i in record:
                table_data = Table_data_info.objects.get(table_data_id=i.table_data_id)
                table_data.delete()
            return DeleteTableRowWithTableRelId(message=f"{table_id} table_id and {table_rel_id} table_rel_id data deleted successfully")
        else:
            return DeleteTableRowWithTableRelId(message=f"{table_id} table_id and {table_rel_id} table_rel_id data is not found")   
            
            
            
class DeleteTableAllDataByTableId(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        table_id = graphene.Int(required=True)
       

    def mutate(self, info, table_id):
        APICALLFUNCTION('DeleteTableAllDataByTableId mutation', 'null')
        record = Table_data_info.objects.filter(table_id=table_id)
        if record:
            for i in record:
                table_data = Table_data_info.objects.get(table_data_id=i.table_data_id)
                table_data.delete()
            return DeleteTableAllDataByTableId(message=f"{table_id} table_id all data deleted successfully")
        else:
            return DeleteTableAllDataByTableId(message=f"{table_id} table_id is not found")            
        
        

class TableDataInput(graphene.InputObjectType):
    table_id = graphene.Int()
    table_col_id = graphene.Int()
    column_data = graphene.String()
    column_name = graphene.String()
    table_ref_id = graphene.String()
    tab_rel_id = graphene.String()
    user_id = graphene.String()
    

class CreateMultipleDynamicTableData(graphene.Mutation):
    table_data_info_type = graphene.List(TableDataInfoType)
    mutation = graphene.Boolean()
    class Input:
       table_data_list = graphene.List(TableDataInput)


    def mutate(self, info, table_data_list):
        APICALLFUNCTION('CreateMultipleDynamicTableData mutation', 'null')
        table_data = []
        for item in table_data_list:
            table_data_list = Table_data_info.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], column_data=item['column_data'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id'], user_id=item['user_id']) 
            table_data.append(table_data_list)
        return CreateMultipleDynamicTableData(mutation=True, table_data_info_type=table_data)   
        

        
class TableDataJsonInput(graphene.InputObjectType):
    table_id = graphene.Int()
    table_col_id = graphene.Int()
    jsonfield = graphene.JSONString()
    column_name = graphene.String()
    table_ref_id = graphene.String()
    tab_rel_id = graphene.String()
    user_id = graphene.String()
    

class CreateMultipleDynamicTableDataJson(graphene.Mutation):
    table_data_dynamic_json_info_type = graphene.List(TableDataJsonDynamicInfoType)
    mutation = graphene.Boolean()
    message = graphene.String()
    class Input:
       table_data_list = graphene.List(TableDataJsonInput)


    def mutate(self, info, table_data_list):
        APICALLFUNCTION('CreateMultipleDynamicTableDataJson mutation', 'null')
        table_data = []
        for item in table_data_list:
            table_data_list = JsonDynamicModel.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], jsonfield=item['jsonfield'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id'], user_id=item['user_id']) 
            table_data.append(table_data_list)
        return CreateMultipleDynamicTableDataJson(mutation=True, message="successfully data save")
        
        

        
    
    
class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()    
    create_course_info = CreateCourseInfo.Field()    
    create_course_master = CreateCourseMaster.Field()    
    create_table_data_info = CreateTableDataInfo.Field()  
    create_table_col_info = CreateTableColInfo.Field() 
    create_crud_info = CRUDInfo.Field()
    create_crud_info_user_id = CRUDInfoUserId.Field()
    user_validation_info = UserValidation.Field()  
    table_data_json_info = TableDataJson.Field()
    user_sign_up = UserSignUp.Field()
    user_sign_up1 = UserSignUp1.Field()
    user_sign_in = UserSignIn.Field()
    user_otp_check = UserOTPCheck.Field()
    create_course_info_dynamic = CreateCourseInfoDynamic.Field()
    create_user_course_mcq_result_dynamic = CreateUserCourseMcqResultDynamic.Field()
    create_event_invitation = CreateEventInvitationDynamic.Field()
    delete_record = DeleteRecord.Field()
    column_data_delete = column_data_delete.Field()
    column_data_update = column_data_update.Field()
    image_upload = ImageUpload.Field()
    add_contact = AddContact.Field()
    create_add_contact = CreateAddContact.Field()
    create_add_device_contact = CreateAddDeviceContact.Field()
    edit_contact = EditContact.Field()
    delete_contact = DeleteContact.Field()
    get_contact = GetContact.Field()
    all_guest = AllGuest.Field()
    event_send_message = SendMessage.Field()
    contact_send_message = ContactSendMessage.Field()
    log_mutation_app = LogMutationApp.Field()
    user_device_info = UserDeviceInfoMutation.Field()
    device_contact = DeviceContactsMutation.Field()
    forget_password_send_email = ForgetPasswordSendEmailMutation.Field()
    change_password_send_email = ChangePasswordSendEmailMutation.Field()
    user_course_mcq_ans = UserCourseMcqAns.Field()
    exam_user_course_mcq_ans = ExamUserCourseMcqAns.Field()
    user_course_chapter = UserCourseChapter.Field()
    course_registration_percentage = CourseRegistrationPercentage.Field()
    course_mcq_final_result = CourseMcqFinalResult.Field()
    exam_course_mcq_final_result = ExamCourseMcqFinalResult.Field()
    table_data_create = TableDataCreate.Field()
    
    
    
    create_table_info_dtl = CreateTableInfoDetail.Field()
    update_table_info_dtl = UpdateTableInfoDetail.Field()
    delete_table_info_dtl = DeleteTableInfoDetail.Field()
    
    create_table_col_info = CreateTableColInfo.Field()
    update_table_col_info = UpdateTableColInfo.Field()
    delete_table_col_info = DeleteTableColInfo.Field()
    
    delete_table_row_with_table_ref_id = DeleteTableRowWithTableRefId.Field()
    delete_table_row_with_table_rel_id = DeleteTableRowWithTableRelId.Field()
    delete_table_all_data_by_table_id = DeleteTableAllDataByTableId.Field()
    
    
    create_multiple_dynamic_table_data = CreateMultipleDynamicTableData.Field()
    create_multiple_dynamic_table_data_json = CreateMultipleDynamicTableDataJson.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    
    
    
class Subscription(graphene.ObjectType):
    table_col_info_subscription = TableColInfoSubcription.Field()      
    
    
    

    
    
    
    