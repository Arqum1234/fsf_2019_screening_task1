
from django.contrib import admin

from .models import User,Team,AllUser

admin.site.register(Team)
admin.site.register(AllUser)
