from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PDF(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
    
