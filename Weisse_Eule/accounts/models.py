from django.db import models
from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    birthday=models.DateField(null=True,blank=True)
