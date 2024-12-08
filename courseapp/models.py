from django.db import models
from slugify import slugify
import os

from datetime import datetime  

# Create your models here.

class course_info(models.Model):
    course_id =  models.AutoField(primary_key=True)
    course_desc = models.CharField(max_length=150, blank=True, null=True)
    course_short_desc = models.CharField(max_length=150, blank=True, null=True)
    course_length = models.CharField(max_length = 150, blank=True, null=True)
    
    
    def __str__(self):
        return self.course_desc

class ccon_desc_master(models.Model):
    cdm_id = models.AutoField( primary_key=True)
    course_id = models.IntegerField(blank=True, null=True)
    ccon_desc_title = models.CharField(max_length=150, blank=True, null=True)
    ccon_desc_sub_title = models.CharField(max_length=150, blank=True, null=True)
    course_slno = models.CharField(max_length=150, blank=True, null=True)
    content_type = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.ccon_desc_title

class ccon_desc_dtl(models.Model):
    cdm_id = models.ForeignKey(ccon_desc_master, on_delete=models.CASCADE)
    cdd_id = models.IntegerField(blank=True, null=True)
    contents_body = models.CharField(max_length=150, blank=True, null=True)
    contents_type = models.CharField(max_length=150, blank=True, null=True)
    image_url	 = models.URLField(max_length=150, blank=True, null=True)
    Image_type = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.contents_body
    
    
    
class ccon_mcq_mst(models.Model):
    cdm_id = models.ForeignKey(ccon_desc_master, on_delete=models.CASCADE)
    mcq_question = models.CharField(max_length=150, blank=True, null=True)
    mcq_type = models.CharField(max_length=150, blank=True, null=True)
    mcq_comments = models.CharField(max_length=150,blank=True, null=True)
    mcq_q_slno = models.CharField(max_length=150, blank=True, null=True)
    mcq_q_multi = models.BooleanField(blank=True, null=True)
    mcq_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.mcq_question

class ccon_mcq_dtl(models.Model):
    mcq_id = models.ForeignKey(ccon_mcq_mst, on_delete=models.CASCADE)
    mcq_choice = models.CharField(max_length=150, blank=True, null=True)
    mcq_choice_slno = models.CharField(max_length=150, blank=True, null=True)
    mcq_choice_type = models.CharField(max_length=150, blank=True, null=True)
    mcq_q_image_url = models.URLField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.mcq_choice
    
    
    
# Dynamic model start

class Table_info_dtl(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=150)
    table_description = models.TextField(max_length=500)
    table_type = models.CharField(max_length=150)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    # table_load = models.FileField()
    
    def __str__(self):
        return self.table_name
    
    

class Table_col_info(models.Model):
    # table_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    table_id = models.IntegerField()
    table_col_id = models.IntegerField(max_length=150)
    column_name = models.CharField(max_length=150)
    col_data_type = models.CharField(max_length=150)
    col_desc = models.TextField(max_length=500)
    # col_source = models.FileField()
    col_classi  = models.CharField(max_length=150)
    col_visible = models.CharField(max_length=50, default="True")
    col_entry_time = models.DateField(auto_now=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    # col_classi_type = models.CharField(max_length=150)
    # col_privs = models.CharField(max_length=150)
    # table_rel_id = models.IntegerField(max_length=150)
    
    def __str__(self):
        return self.column_name

class Table_data_info(models.Model):
    table_data_id = models.AutoField(primary_key=True)
    slno = models.IntegerField(blank=True, null=True)
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    # table_ref_id = models.IntegerField(default=1)
    table_ref_id = models.CharField(max_length=250, default=1)
    tab_rel_id = models.CharField(max_length=150, blank=True, null=True)
    user_id = models.CharField(max_length=150, blank=True, null=True)
    vflag = models.CharField(max_length=150, blank=True, null=True)
    # table_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    # table_col_id = models.ForeignKey(Table_col_info, on_delete=models.CASCADE)
    column_data	= models.TextField()
    col_data_type = models.CharField(max_length=150)
    column_name	 = models.CharField(max_length=150)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    
    # table_id = models.IntegerField()
    # table_data_id = models.IntegerField()

    
    
    def __str__(self):
        return self.column_data
        
        


class Table_info_dtl2(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=150)
    table_description = models.TextField(max_length=500)
    table_type = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.table_name
    
    

class Table_col_info2(models.Model):
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    column_name = models.CharField(max_length=150)
    col_data_type = models.CharField(max_length=150)
    col_desc = models.TextField(max_length=500)
    col_classi  = models.CharField(max_length=150)
    col_visible = models.CharField(max_length=50, default="True")
    col_entry_time = models.DateField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.column_name
    
class Table_data_info2(models.Model):
    table_data_id = models.AutoField(primary_key=True)
    slno = models.IntegerField(blank=True, null=True)
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    table_ref_id = models.CharField(max_length=250, default=1)
    tab_rel_id = models.CharField(max_length=150, blank=True, null=True)
    user_id = models.CharField(max_length=150, blank=True, null=True)
    vflag = models.CharField(max_length=150, blank=True, null=True)
    column_data	= models.TextField()
    col_data_type = models.CharField(max_length=150)
    column_name	 = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.column_data}" 




class Table_info_dtl3(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=150)
    table_description = models.TextField(max_length=500)
    table_type = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.table_name
    
    

class Table_col_info3(models.Model):
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    column_name = models.CharField(max_length=150)
    col_data_type = models.CharField(max_length=150)
    col_desc = models.TextField(max_length=500)
    col_classi  = models.CharField(max_length=150)
    col_visible = models.CharField(max_length=50, default="True")
    col_entry_time = models.DateField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.column_name
    
class Table_data_info3(models.Model):
    table_data_id = models.AutoField(primary_key=True)
    slno = models.IntegerField(blank=True, null=True)
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    table_ref_id = models.CharField(max_length=250, default=1)
    tab_rel_id = models.CharField(max_length=150, blank=True, null=True)
    user_id = models.CharField(max_length=150, blank=True, null=True)
    vflag = models.CharField(max_length=150, blank=True, null=True)
    column_data	= models.TextField()
    col_data_type = models.CharField(max_length=150)
    column_name	 = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.column_data}" 

        
        
# Dynamic model end        
        
        
        
def upload_file_path(instance, filename):
    upload_file_name = slugify(instance.name)
    upload_file_date = slugify(instance.date)
    _, extension = os.path.splitext(filename)
    return f"upload_file/images/{upload_file_name}{upload_file_date}{extension}"



class UploadFile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to=upload_file_path, blank=True, null=True) 
    
    def __str__(self):
        return self.name
        
        
def upload_file_path_invitation(instance, filename):
    upload_file_name = slugify(instance.name)
    upload_file_date = slugify(instance.date)
    _, extension = os.path.splitext(filename)
    return f"upload_file/invitation_event/images/{upload_file_name}{upload_file_date}{extension}"



class InvitationEventUploadFile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to=upload_file_path_invitation, blank=True, null=True)
    
    
    def __str__(self):
        return self.name  
        
        
def upload_file_path_csv(instance, filename):
    upload_file_name = slugify(instance.name)
    _, extension = os.path.splitext(filename)
    print("226", extension)
    return f"upload_file/excel/{upload_file_name}{extension}"

class CSVUploadFile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to=upload_file_path_csv, blank=True, null=True)
    
    def __str__(self):
        return self.name    
        
        
        
def upload_file_path_json(instance, filename):
    upload_file_name = slugify(instance.name)
    _, extension = os.path.splitext(filename)
    return f"upload_file/node-design/{upload_file_name}{extension}"

class JsonUploadFile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to=upload_file_path_json, blank=True, null=True)
    
    def __str__(self):
        return self.name         
        
        
        
        
class JsonModel(models.Model):
    jsonfield = models.JSONField(blank=True, null=True)     
    
    
class JsonDynamicModel(models.Model):
    table_data_id = models.AutoField(primary_key=True)
    table_id = models.IntegerField()
    table_col_id = models.IntegerField()
    table_ref_id = models.CharField(max_length=250, default=1)
    tab_rel_id = models.CharField(max_length=150, blank=True, null=True)
    user_id = models.CharField(max_length=150, blank=True, null=True)
    col_data_type = models.CharField(max_length=150, default='String')
    column_name	 = models.CharField(max_length=150)
    jsonfield = models.JSONField(blank=True, null=True) 
    
    def __str__(self):
        return f'{self.jsonfield}'    
    
    
    
    
              

    
    
    