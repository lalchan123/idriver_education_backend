# Rest Framework Import
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
# from rest_framework.response import Response


# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler

# from .Casual import CasualFunction

# from courseapp.models import Table_data_info

# import logging

# logger = logging.getLogger(__name__)
# # logger = logging.getLogger('django')
# logger.debug('1157 Find result! logger')
# print("1157 Find result! print")

# # from django_apscheduler.jobstores import DjangoJobStore, register_events

# # scheduler1 = BackgroundScheduler()

# # # @scheduler1.scheduled_job('interval', id='my_job_id', seconds=5)
# # @scheduler1.scheduled_job('interval', id='my_job_id', minutes=1)
# # def JobSearch():
# # 	CasualFunction()
# # scheduler1.start()

# def JobSearch():
#     # scheduler = BackgroundScheduler()
#     # # scheduler =  BlockingScheduler()
#     # scheduler.add_jobstore(DjangoJobStore(), "default")
#     # scheduler.add_job(CasualFunction, 'cron', minute=1)
#     # # 	scheduler.add_job(CasualFunction, 'interval', seconds=20)
#     # # register_events(scheduler)
#     # scheduler.start()
#     try:
        
#         # scheduler = BackgroundScheduler()
#         # scheduler.add_job(CasualFunction, 'cron', minute=1)
#         # scheduler.start()
        
#         print("scheduler")
        
        
#     except Exception as err:
#         return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)