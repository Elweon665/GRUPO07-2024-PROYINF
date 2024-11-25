from django.db import models

class Scrap(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
        
    def __str__(self):
        return str(self.title) + " " + str(self.link) + " " + str(self.content)

