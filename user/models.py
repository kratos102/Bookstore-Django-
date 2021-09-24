from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    phone_number = models.CharField(default='', max_length=15)
    address = models.CharField(default='', max_length= 255)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False)