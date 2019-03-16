"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from teams import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^signup/$',views.signup_view,name='signup'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^teams-and-tasks-list/$',views.teamsandtasks_view,name="teams"),
    url(r'^create-team-name/$',views.createteamname_view,name="createteamname"),
    url(r'^team/(?P<pk>[0-9]+)/$', views.team_view,name="team"),
    url(r'^(?P<username>[a-zA-Z]+)/create-task/$',views.create_my_task_view,name="createMyTask"),
    url(r'^(?P<username>[a-zA-Z]+)/task/(?P<id>[0-9]+)/$',views.my_task_view,name="mytask"),
    url(r'^(?P<username>[a-zA-Z]+)/task/(?P<id>[0-9]+)/edit/$',views.my_task_edit_view,name="myTaskEdit"),
    url(r'^team/(?P<team_id>[0-9]+)/create-task$', views.team_create_task_view,name="createTeamTask"),
    url(r'^team/(?P<team_id>[0-9]+)/(?P<taskname>[a-zA-Z]+)/$', views.team__task_view,name="teamTask"),
    url(r'^team/(?P<team_id>[0-9]+)/(?P<taskname>[a-zA-Z]+)/edit$', views.team_task_edit_view,name="teamTaskEdit"),
    url(r'^team/(?P<team_id>[0-9]+)/(?P<taskname>[a-zA-Z]+)/modify$', views.team_task_modify_view,name="teamTaskModify"),


]
