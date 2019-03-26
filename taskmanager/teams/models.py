from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    team_name=models.CharField(max_length=100,unique=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)


class AllUser(models.Model):
    team= models.ForeignKey(Team,on_delete=models.CASCADE,default=None)
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=None)


class TaskDetail(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    assignedBy = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class TeamTask(models.Model):
    taskDetail = models.ForeignKey(TaskDetail,on_delete=models.CASCADE,default=None)
    assignee = models.CharField(max_length=100)
    assigned = models.BooleanField(default=False)

class MyTask(models.Model):
    taskOwner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100)

class TeamTaskComment(models.Model):
    taskDetail = models.ForeignKey(TaskDetail,on_delete=models.CASCADE,default=None)
    comment = models.CharField(max_length=500)
    commentedBy = models.CharField(max_length=100)


class MyTaskComment(models.Model):
    taskOwner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    taskName = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)


# Create your models here.
