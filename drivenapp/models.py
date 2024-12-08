from django.db import models

# Create your models here.

class skeleton_master(models.Model):
    sk_id = models.AutoField(primary_key=True)
    sk_desc = models.CharField(max_length=150)
    sk_comments = models.CharField(max_length=150)
    sk_page = models.CharField(max_length=150)
    sk_place = models.CharField(max_length=150)
    sk_until = models.CharField(max_length=150)
    sk_loc= models.CharField(max_length=150)

    def __str__(self):
        return self.sk_desc
    
class skeleton_detail(models.Model):
    sk_id = models.ForeignKey(skeleton_master, on_delete=models.CASCADE)
    sk_did  = models.CharField(max_length=150)
    sk_attr_name = models.CharField(max_length=150)
    sk_attr_value1 = models.CharField(max_length=150)
    sk_attr_value2 = models.CharField(max_length=150)
    
    def __str__(self):
            return self.sk_attr_name