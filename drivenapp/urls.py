from django.urls import path, include

from drivenapp.views import *

# import routers from the REST framework
# it is necessary for routing
from rest_framework import routers
 
# create a router object
router = routers.DefaultRouter()
 
# register the router
router.register(r'skeleton_master', skeleton_master_view, 'skeleton_master')
router.register(r'skeleton_detail', skeleton_detail_view, 'skeleton_detail')

urlpatterns = [
    path('',templateCheck, name="templateCheck"),
    path('api/', include(router.urls)),
]
