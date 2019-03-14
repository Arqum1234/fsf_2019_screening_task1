from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    team_name=models.CharField(max_length=100,unique=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)


class AllUser(models.Model):
    team= models.ForeignKey(Team,on_delete=models.CASCADE,default=None)
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=None)

class Task(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    assignedBy = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100)
    
# Create your models here.
