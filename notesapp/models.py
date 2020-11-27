from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    textnote=models.CharField(max_length=10000)
    user=models.ForeignKey(User,db_column='username',on_delete=models.CASCADE)
    time=models.DateTimeField()
    def __str__(self):
        return str(self.id)