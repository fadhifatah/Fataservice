from django.db import models


# Create your models here.
class User1(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    display_name = models.CharField(max_length=250)
    secret = models.CharField(max_length=100)
