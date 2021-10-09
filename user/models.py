from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False)