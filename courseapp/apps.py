from django.apps import AppConfig
# from courseapp.Scheduler.StartCausal import *

class CourseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courseapp'
    
    # def ready(self):
    #     from courseapp.Scheduler import StartCausal
    #     StartCausal.JobSearch() 

