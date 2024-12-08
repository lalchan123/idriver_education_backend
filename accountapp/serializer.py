from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from accountapp.models import *
from courseapp.models import *


# user serializer start
class UserMasterSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User,
        fields = ['id','username','email','role','password','isAdmin']
        

    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff
    
    

class UserMasterSerializerWithToken(UserMasterSerializer):
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =User
        fields = ['id','username','email','role','password','is_active','isAdmin','token']
        

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token) 
    


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'
        
        
class SampleSerializer1(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    is_active = serializers.CharField()
    
    
# class JsonDataSerializer(serializers.Serializer):
#     json_data = serializers.SerializerMethodField()
#     class Meta:
#         model = Table_data_info
#         fields = '__all__'
#     def get_json_data(self, obj):
#         return obj    
    
# user serializer end




class GETDynamicTableJsonFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonDynamicModel
        fields = '__all__'