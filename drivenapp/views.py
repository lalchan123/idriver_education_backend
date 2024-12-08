from django.shortcuts import render

# import view sets from the REST framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

# serializer
from drivenapp.serializers import *

# models
from drivenapp.models import *

# Create your views here.

def templateCheck(request):
    return render(request, 'index.html',)

class skeleton_master_view(viewsets.ModelViewSet):
    serializer_class = skeleton_master_serializer
    queryset = skeleton_master.objects.all()
    
class skeleton_detail_view(viewsets.ModelViewSet):
    serializer_class = skeleton_detail_serializer
    queryset = skeleton_detail.objects.all()
