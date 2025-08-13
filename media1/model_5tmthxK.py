from django.db import models

# Create your models here.

class Table_info_dtl(models.Model):
    table_id = models.AutoField( primary_key=True)
    table_name = models.CharField(max_length=150)
    table_description = models.TextField(max_length=500)
    table_type = models.CharField(max_length=150)
    table_load = models.FileField()

class  Table_col_info(models.Model):
    table_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    table_col_id = models.IntegerField(max_length=150)
    column_name = models.CharField(max_length=150)
    col_data_type = models.CharField(max_length=150)
    col_desc = models.TextField(max_length=500)
    col_source = models.FileField()
    col_classi  = models.CharField(max_length=150)
    col_classi_type = models.CharField(max_length=150)
    col_privs = models.CharField(max_length=150)
    table_rel_id = models.IntegerField(max_length=150)

class Table_data_info(models.Manager):
    table_col_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    column_data	= models.TextField(max_length=500)
    col_data_type = models.CharField(max_length=150)
    column_name	 = models.CharField(max_length=150)
    table_data_id = models.IntegerField(max_length=150)

class Table_rel_info(models.Model):
    table_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    table_col_id_from = models.IntegerField(max_length=150)
    table_rel_id = models.IntegerField(max_length=150)
    table_col_id_to = models.IntegerField(max_length=150)
    rel_type = models.CharField(max_length=150)

class Table_col_constraints(models.Model):
    table_col_con_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    table_col_id =  models.IntegerField(max_length=150)
    con_type = models.CharField(max_length=150)
    con_logic = models.CharField(max_length=150)

class Table_role_info(models.Model):
    table_role_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    sentry_role = models.CharField(max_length=150)
    entry_role_type = models.CharField(max_length=150)
    sentry_role_logic = models.CharField(max_length=150)
    table_id = models.IntegerField(max_length=150)

class User_role_info(models.Model):
    user_id = models.ForeignKey(Table_info_dtl, on_delete=models.CASCADE)
    table_role_id = models.IntegerField(max_length=150)


def __str__(self):
    return self.table_name
