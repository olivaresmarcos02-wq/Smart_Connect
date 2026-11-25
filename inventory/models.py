from django.db import models

# Create your models here.

class Equipment(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
