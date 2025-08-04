from django.urls import path

from courseapp.views import *

urlpatterns = [
    path('upload_file_apiview/', UploadFileAPIView.as_view()),
    path('invitation_event_upload_file_apiview/', InvitationEventUploadFileAPIView.as_view()),
    path('upload_image_react_file_pond_apiview/', UploadImageReactFilePondView.as_view()),
    path('csv_upload_file_apiview/', CSVUploadFileAPIView.as_view()),
    path('json_upload_file_apiview/', JSONUploadFileAPIView.as_view()),
    path('change_password/<email>/', ForgetPasswordConfirm, name='forget_change_password'),
    path('change-password/<email>/', ChangePasswordConfirm, name='change_password'),
    path('driver-activate-mail/<email>/', DriverActivationMail , name='driver_activate_mail'),
    path('user-activate-mail/<str:email_or_username_or_phone_number>/', UserActivationMail , name='user_activate_mail'),
    path('scheduler/', SchedulerApiView),
    path('scheduler-queue/', SchedulerQueueApiView),
    path('datastore/<str:server_name>/', DataStoreView),
    path('process-status-change/', ProcessStatusChangeView),
    path('process-status-update/', ProcessStatusUpdateView),
    path('datastore-process/', DataStoreProcessView),
]