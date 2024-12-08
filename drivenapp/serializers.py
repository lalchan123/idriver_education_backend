# import serializers from the REST framework
from dataclasses import fields
from rest_framework import serializers

from drivenapp.models import *

# skeleton_master serializer
class skeleton_master_serializer(serializers.ModelSerializer):
    class Meta:
        model = skeleton_master
        fields = '__all__'
        

# skeleton_detail serializer
class skeleton_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = skeleton_detail
        fields = '__all__'        