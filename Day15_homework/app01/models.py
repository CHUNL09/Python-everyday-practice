from django.db import models

# Create your models here.
class userinfo(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64)

class host(models.Model):
    hostname=models.CharField(max_length=32)
    ip=models.CharField(max_length=32)
    port=models.CharField(max_length=8)
    status=models.CharField(max_length=10)