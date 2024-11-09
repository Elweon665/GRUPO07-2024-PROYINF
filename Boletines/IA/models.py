from django.db import models
from HomePage.models import User

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100)
    

class Boletin_Petition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boletin = models.ForeignKey(Petition, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'boletin']
        
    def __str__(self):
        return self.name

