from django.db import models

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