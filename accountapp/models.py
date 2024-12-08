from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# custom user model start
    
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user
      
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)  
        return user    
       
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)    
        extra_fields.setdefault('is_superuser', True)    
        extra_fields.setdefault('is_active', True)    
        extra_fields.setdefault('role', 'Admin')      
        extra_fields.setdefault('is_email_varified', True)    

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The superuser must have is_staff True.')

        return self._create_user( email, password, **extra_fields)    
       

Role =(
    ('Admin','Admin'),
    ('Driver','Driver'),
)

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=255, unique=True, null=True, blank = True,)
    role = models.CharField(max_length=40, null=True, blank = True, choices=Role )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 
    is_email_varified =models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
   
    
    
    def __str__(self):
        return f'{self.email}'
    
    
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank = True)
    last_name = models.CharField(max_length=200, null=True, blank = True)
    zip_code = models.CharField(max_length=200, null=True, blank = True)
    
    
    
    def __str__(self):
        return self.first_name
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
# custom user model end  