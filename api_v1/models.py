from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    display_name = models.CharField(max_length=500)


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
