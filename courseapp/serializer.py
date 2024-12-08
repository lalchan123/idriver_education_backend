from rest_framework import serializers
from courseapp.models import *



class UploadFileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = UploadFile
        fields = ['name', 'date', 'file_name']
        
        
        
class InvitationEventUploadFileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = InvitationEventUploadFile
        fields = ['name', 'date', 'file_name']   
        
class CSVUploadFileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = CSVUploadFile
        fields = ['name',  'file_name'] 
        
        
class JSONUploadFileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = JsonUploadFile
        fields = ['name',  'file_name']        