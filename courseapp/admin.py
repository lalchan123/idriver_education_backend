from django.contrib import admin

from courseapp.models import *

# # Register your models here.

admin.site.register(ccon_desc_master)
admin.site.register(ccon_desc_dtl)
admin.site.register(course_info)
admin.site.register(ccon_mcq_mst)
admin.site.register(ccon_mcq_dtl)

admin.site.register(Table_info_dtl)
admin.site.register(Table_col_info)
admin.site.register(Table_data_info)

admin.site.register(Table_info_dtl2)
admin.site.register(Table_col_info2)
admin.site.register(Table_data_info2)

admin.site.register(Table_info_dtl3)
admin.site.register(Table_col_info3)
admin.site.register(Table_data_info3)

admin.site.register(UploadFile)
admin.site.register(CSVUploadFile)
admin.site.register(JsonUploadFile)
admin.site.register(InvitationEventUploadFile)
admin.site.register(JsonModel)
admin.site.register(JsonDynamicModel)
