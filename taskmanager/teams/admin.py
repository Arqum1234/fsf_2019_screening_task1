
from django.contrib import admin

from .models import User,Team,AllUser,TeamTask,MyTask,TaskDetail

admin.site.register(Team)
admin.site.register(AllUser)
admin.site.register(TeamTask)
admin.site.register(MyTask)
admin.site.register(TaskDetail)
