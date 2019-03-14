from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    team_name=models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)


class AllUser(models.Model):
    team= models.ForeignKey(Team,on_delete=models.CASCADE,default=None)
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=None)


# Create your models here.
