
from django.contrib import admin

from .models import User,Team,AllUser,TeamTask,MyTask,TaskDetail,TeamTaskComment,MyTaskComment

admin.site.register(Team)
admin.site.register(AllUser)
admin.site.register(TeamTask)
admin.site.register(MyTask)
admin.site.register(TaskDetail)
admin.site.register(TeamTaskComment)
admin.site.register(MyTaskComment)
