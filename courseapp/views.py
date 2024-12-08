from django.shortcuts import redirect, render

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib import messages


import time
from datetime import datetime, timedelta


from courseapp.models import *
from courseapp.serializer import *

from courseapp.Scheduler.StartCausal import *
from courseapp.Scheduler.Casual import JobStart, QueueFunction
from accountapp.DynamicFunction.Process_Log import ProcessLogFunction

# global function
from FunctionFolder.WrapperFunc import *

# Create your views here.

# JobSearch()


@api_view(['POST'])
def SchedulerApiView(request):
    try:
        APICALLFUNCTION('SchedulerApiView', 'null')
        JobStart() 
        return Response({'message':"success",'status': status.HTTP_200_OK, "data": "success"})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def SchedulerQueueApiView(request):
    try:
        APICALLFUNCTION('SchedulerQueueApiView', 'null')
        QueueFunction() 
        return Response({'message':"success",'status': status.HTTP_200_OK, "data": "Scheduler Queue started success"})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)        
        
        
    
class UploadFileAPIView(APIView):  
    def post(self,request):
        APICALLFUNCTION('UploadFileAPIView', 'null')
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        
        
class InvitationEventUploadFileAPIView(APIView):  
    def post(self,request):
        APICALLFUNCTION('InvitationEventUploadFileAPIView', 'null')
        serializer = InvitationEventUploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        
class CSVUploadFileAPIView(APIView):  
    def post(self,request):
        APICALLFUNCTION('CSVUploadFileAPIView', 'null')
        serializer = CSVUploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class JSONUploadFileAPIView(APIView):  
    def post(self,request):
        APICALLFUNCTION('JSONUploadFileAPIView', 'null')
        serializer = JSONUploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        
        
@api_view(['GET'])   
def DriverActivationMail(request, email):
    APICALLFUNCTION('DriverActivationMail', 'null')
    
    if email:
        email_detail = Table_data_info.objects.get(table_id=1, column_data=email)
        flag = Table_data_info.objects.filter(table_id=1, table_ref_id=email_detail.table_ref_id, user_id=email_detail.user_id)

        for i in flag:
            if i.table_col_id==6 and i.column_name=="is_email_verified" and i.column_data=="False":
                flag_detail_email_activation = Table_data_info.objects.get(table_id=1, table_col_id=i.table_col_id, column_data=i.column_data, column_name=i.column_name, table_ref_id=i.table_ref_id, user_id=i.user_id)
                flag_detail_email_activation.column_data="True"
                flag_detail_email_activation.save()
                
            if i.table_col_id==4 and i.column_name=="is_active" and i.column_data=="False":
                user_active = Table_data_info.objects.get(table_id=1, table_col_id=i.table_col_id, column_data=i.column_data, column_name=i.column_name, table_ref_id=i.table_ref_id, user_id=i.user_id)
                user_active.column_data="True"
                user_active.save()
                
                
        Event_Detail_list = Table_data_info.objects.filter(table_id=4, user_id=email) 
        if Event_Detail_list:
            for i in Event_Detail_list:
                i.user_id = email_detail.user_id
                i.save()   

        User_Contact_list = Table_data_info.objects.filter(table_id=6, user_id=email) 
        if User_Contact_list:
            for i in User_Contact_list:
                i.user_id = email_detail.user_id
                i.save() 

        Event_Contact_list = Table_data_info.objects.filter(table_id=5, user_id=email) 
        if Event_Contact_list:
            for i in Event_Contact_list:
                i.user_id = email_detail.user_id
                i.save()        
                       
        
        return render(request, "activation_welcome_page.html")
    else:
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Activation link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
def ForgetPasswordConfirm(request, email):
    try:
        if request.method == 'POST':
            APICALLFUNCTION('ForgetPasswordConfirm', 'null')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not Table_data_info.objects.filter(column_data=email, table_id=1).first():
                messages.success(request, "Email is not valid, Please enter your valid email")
                return render(request, "change_password_page.html")            

            if new_password != confirm_password:
                messages.success(request, "new password and confirm password donot match")
                return render(request, "change_password_page.html")            

            user = Table_data_info.objects.get(column_data=email, table_id=1)
            flag = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
            for i in flag:
                if i.table_col_id==2 and i.column_name=="password":
                    
                    password_change = Table_data_info.objects.get(table_id=1, table_col_id=i.table_col_id, column_data=i.column_data, column_name=i.column_name, table_ref_id=i.table_ref_id, user_id=i.user_id)
                    password_change.column_data=new_password
                    password_change.save()

                    return render(request, "password_change_welcome_page.html") 
                        
              
    except Exception as e:  
        print(e)  
        messages.success(request, "Something Wrong")
    return render(request, "change_password_page.html")
    
    
def ChangePasswordConfirm(request, email):
    try:
        APICALLFUNCTION('ChangePasswordConfirm', 'null')
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not Table_data_info.objects.filter(column_data=email, table_id=1).first():
                messages.success(request, "Email is not valid, Please enter your valid email")
                return render(request, "change_password_page_idriven.html") 
                
            if old_password:
                user = Table_data_info.objects.get(column_data=email, table_id=1)
                if not Table_data_info.objects.filter(column_data=old_password, table_id=1, table_col_id=2, table_ref_id=user.table_ref_id, user_id=user.user_id):
                    messages.success(request, "Old password is not valid, Please enter your valid old password")
                    return render(request, "change_password_page_idriven.html")    
                
            if new_password != confirm_password:
                messages.success(request, "new password and confirm password donot match")
                return render(request, "change_password_page_idriven.html")            

            user = Table_data_info.objects.get(column_data=email, table_id=1)
            flag = Table_data_info.objects.filter(table_id=1, table_ref_id=user.table_ref_id, user_id=user.user_id)
            for i in flag:
                if i.table_col_id==2 and i.column_name=="password":
                    
                    password_change = Table_data_info.objects.get(table_id=1, table_col_id=i.table_col_id, column_data=i.column_data, column_name=i.column_name, table_ref_id=i.table_ref_id, user_id=i.user_id)
                    password_change.column_data=new_password
                    password_change.save()

                    return render(request, "password_change_welcome_page.html") 
                        
              
    except Exception as e:  
        print(e)  
        messages.success(request, "Something Wrong")
    return render(request, "change_password_page_idriven.html")            
    
        
        



@api_view(['GET'])
def DataStoreView(request, server_name):
    try:
        APICALLFUNCTION('DataStoreView', 'null')
        sections = {}
        items = []
        refId = []
        casual_data = Table_data_info.objects.filter(table_id=542)
        for k in casual_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))

        for m in refId:
            for i in casual_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}
        
        
        unprocess_data = [x for x in items if x['Process_Status'] == 'unprocess' and x['Server_Name'] == server_name]
        
        inprocess_data = [x for x in items if x['Process_Status'] == 'Inprogress' and x['Server_Name'] == server_name]
        
        return Response({'message':"success",'status': status.HTTP_200_OK, "unprocess_data": unprocess_data, "inprocess_data": inprocess_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)        
        
        
@api_view(['GET'])
def DataStoreProcessView(request):
    try:
        # APICALLFUNCTION('DataStoreView', 'null')
        fileName = main_media_url+f'/media/upload_file/investing/json/casual_process.json'
        fileName2 = main_media_url+f'/media/upload_file/investing/json/casual_process_code.json'
        casual_data=""
        casual_process_code=""
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            casual_data = data['data']

        if os.path.isfile(fileName2):
            f = open(fileName2)
            data = json.load(f)
            casual_process_code = data['data']

        return Response({'message':"success",'status': status.HTTP_200_OK, "casual_data": casual_data, "casual_process_code": casual_process_code})

            # print("casual_code", casual_code)  
        #     job_data = [x for x in casual_code if x['Process_Name'] == job_name]
        
        
        # unprocess_data = [x for x in items if x['Process_Status'] == 'unprocess']

        # inprocess_data = [x for x in items if x['Process_Status'] == 'Inprogress']

        # return Response({'message':"success",'status': status.HTTP_200_OK, "unprocess_data": unprocess_data, "inprocess_data": inprocess_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)                        
        
# @api_view(['GET'])
# def DataStoreProcessView(request):
#     try:
#         # APICALLFUNCTION('DataStoreView', 'null')
#         sections = {}
#         items = []
#         refId = []
#         casual_data = Table_data_info.objects.filter(table_id=542)
#         for k in casual_data:
#             refId.append(k.table_ref_id)
                   
#         refId = list(set(refId))
#         for m in refId:
#             for i in casual_data:
#                 if i.table_ref_id==m:
#                     sections[i.column_name]=i.column_data
#                     sections['table_ref_id']=i.table_ref_id
#             if sections != "":
#                 items.append(sections)   
#                 sections = {}
        
        
#         unprocess_data = [x for x in items if x['Process_Status'] == 'unprocess']

#         inprocess_data = [x for x in items if x['Process_Status'] == 'Inprogress']

#         return Response({'message':"success",'status': status.HTTP_200_OK, "unprocess_data": unprocess_data, "inprocess_data": inprocess_data})
#     except Exception as err:
#         return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)                        
        
        
@api_view(['POST'])
def ProcessStatusChangeView(request):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    data=request.data                    
    try:
        APICALLFUNCTION('ProcessStatusChangeView', 'null')
        
        process_data = Table_data_info.objects.filter(table_id=542, table_ref_id=data['table_ref_id'])
        if len(process_data)!=0:
            for pd in process_data:
                if pd.table_col_id == 7:
                    process_update_data = Table_data_info.objects.get(table_id=542, table_col_id=pd.table_col_id, table_ref_id=pd.table_ref_id)
                    process_update_data.column_data = data['Process_Status']
                    process_update_data.save()
        return Response({"message": "Process Status Change Successfully", 'status': status.HTTP_200_OK})

    except Exception as err:
        ProcessLogFunction(process_id=data['Process_Id'], log_date=currenttimedate, log_output_file="", log_data_type="error with server2", log_process_name=data['Process_Name'], error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def ProcessStatusUpdateView(request):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    data=request.data                    
    try:
        APICALLFUNCTION('ProcessStatusUpdateView', 'null')
        
        process_data = Table_data_info.objects.filter(table_id=542, table_ref_id=data['table_ref_id'])
        if len(process_data)!=0:
            for pd in process_data:
                if pd.table_col_id == 7:
                    process_update_data = Table_data_info.objects.get(table_id=542, table_col_id=pd.table_col_id, table_ref_id=pd.table_ref_id)
                    process_update_data.column_data = "Done"
                    process_update_data.save()
                    
        return Response({"message": "Process Status Update Done Successfully", 'status': status.HTTP_200_OK})

    except Exception as err:
        ProcessLogFunction(process_id=data['Process_Id'], log_date=currenttimedate, log_output_file="", log_data_type="error with server2", log_process_name=data['Process_Name'], error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        