
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .models import User,Team,AllUser,TeamTask,MyTask,TaskDetail

def home(request):

    return render(request,'homepage.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save()
            #log the user
            login(request,user)
            return redirect('teams')
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{'form':form})
# Create your views here.

def login_view(request):
    if request.method == 'POST' :
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() :
            #log the user in
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('teams')
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def teamsandtasks_view(request):
    myTeams = Team.objects.filter(owner=request.user)
    memberTeams = AllUser.objects.filter(user=request.user)

    memberTeamName=[]
    for memberTeam in memberTeams:
        memberTeamName.append(memberTeam.team)
    myTasks = MyTask.objects.filter(taskOwner=request.user)
    # print(myTeams)
    # print(memberTeams)

    return render(request,'teamstasks_list.html',{'myTeams':myTeams,'memberTeamName':memberTeamName,'request':request,'myTasks':myTasks})

def team_view(request,pk):
    message=""
    teamname=Team.objects.filter(id=pk)[0].team_name
    if request.method=="POST":
        username=request.POST.get('username')
        users=User.objects.filter(username=username)
        #print(users)
        if len(users) > 0:

            #print(teamname)
            #print(User.objects.filter(username=username))
            #print(Team.objects.filter(team_name=teamname))
            exists=AllUser.objects.filter(user=User.objects.get(username=username)).filter(team=Team.objects.get(team_name=teamname))
            #print(exists)
            if request.user.username==username:
                message="You cannot add yourself!!!"
            elif len(exists)>0:
                message="User is already added to the team!!!"
            else:
                user = User.objects.get(username=username)
                team = Team.objects.get(team_name=teamname)
                obj=AllUser(user=user,team=team)
                obj.save()
        else:
            message="User does not exists!!!"
    members=AllUser.objects.filter(team=Team.objects.get(team_name=teamname))
    flag=1
    ownerUserName=Team.objects.get(team_name=teamname).owner.username
    #print(members)
    #if len(members==0):flag=0

    team=Team.objects.get(id=pk)
    tasksByMe = TaskDetail.objects.filter(team=team).filter(assignedBy=request.user.username)
    # tasksForMe=TaskDetail.objects.filter(team=team)
    # if tasksForMe.count()>0:
    #     tasksForMe = TeamTask.objects.filter(taskDetail=TaskDetail.objects.filter(team=team).get(title=teamname)).filter(assignee=request.user.username)
    tasksForMe=[]
    taskDetails = TaskDetail.objects.filter(team=team)
    for taskDetail in taskDetails:
        obj=TeamTask.objects.filter(taskDetail=taskDetail).filter(assignee=request.user.username).filter(assigned=True)
        if len(obj)>0:
            tasksForMe.append(obj[0])
    exc=[]
    for taskForMe in tasksForMe:
        exc.append(taskForMe.taskDetail)
    otherTasks = TaskDetail.objects.exclude(pk__in=tasksByMe.values_list('pk', flat=True)).exclude(id__in=[ex.id for ex in exc])

    # else:
    #     otherTasks = TaskDetail.objects.exclude(pk__in=tasksByMe.values_list('pk', flat=True))
    otherTasks = otherTasks.filter(team=team)
    flag1=0
    flag2=0
    flag3=0
    if tasksByMe.count()>0:
        flag1=1
    if len(tasksForMe)>0:
        flag2=1
    if otherTasks.count()>0:
        flag3=1

    return render(request,'team.html',{'message':message,'id':pk,'members':members,
    'flag':flag,'ownerUserName':ownerUserName,'request':request,
    'tasksByMe':tasksByMe,'tasksForMe':tasksForMe,'otherTasks':otherTasks,
    'flag1':flag1,'flag2':flag2,'flag3':flag3})


def createteamname_view(request):
    message=""
    if request.method=='POST':
        teamname=request.POST.get('teamname')
        t = Team(team_name = teamname,owner = request.user)
        try:
            t.save()
            pk = t.id
            return redirect('team',pk)
        except:
            message="Team name already exists!!!"
            if request.method=='GET':
                message=""
            return render(request,'createteamname.html',{'message':message})
    else:
        return render(request,'createteamname.html',{'message':message})


def create_my_task_view(request,username):
    message=""
    if request.method=='POST':
        title=request.POST.get('taskname')
        description=request.POST.get('description')
        taskOwner=request.user
        exists=MyTask.objects.filter(title=title).filter(taskOwner=request.user)
        if len(exists)>0:
            message="You already have a task with that name!!!"
        else:
            obj=MyTask(taskOwner=taskOwner,title=title,description=description)
            obj.save()
            id=obj.id
            return redirect('mytask',username,id)
    return render(request,'create_my_task.html',{'message':message,'request':request})

def my_task_view(request,username,id):
    myTask = MyTask.objects.get(id=id)
    return render(request,'my_task.html',{'myTask':myTask,'request':request})

def my_task_edit_view(request,username,id):
    message=""
    if request.method=='POST':
        obj=MyTask.objects.get(id=id)

        title=request.POST.get('taskname')
        description=request.POST.get('description')
        exists=MyTask.objects.filter(title=title).filter(taskOwner=request.user)

        if len(exists)>0 and obj.title!=title:
            message="You already have a task with that name!!!"
        else:
            obj.title=title
            obj.description=description
            obj.save()
            return redirect('mytask',username,id)
    return render(request,'my_task_edit.html',{'message':message,'request':request,'id':id})

def team_create_task_view(request,team_id):
    message=""
    if request.method=='POST':
        team=Team.objects.get(id=team_id)
        title=request.POST.get('taskname')
        description=request.POST.get('description')
        assignee=request.POST.get('assignee')
        exists = User.objects.filter(username=assignee)
        print(len(exists))
        if len(exists)>0:
            exists = AllUser.objects.filter(team=team).filter(user=User.objects.get(username=assignee))
        if request.user.username == assignee or len(exists)>0 :
            taskExists = TaskDetail.objects.filter(team=team).filter(title=title)
            if len(taskExists)>0:
                message="Task title exists!!"
            else:
                teamMembers = AllUser.objects.filter(team=team)
                i=0
                objTask = TaskDetail(team=team,title=title,description=description,assignedBy=request.user.username)
                objTask.save()
                print(len(teamMembers))
                for teamMember in teamMembers:
                    if teamMember.user.username == assignee:
                        obj = TeamTask(taskDetail=objTask,assignee=assignee,assigned=True)
                        obj.save()
                        i=i+1
                    else:
                        obj = TeamTask(taskDetail=objTask,assignee=teamMember.user.username,assigned=False)
                        obj.save()
                if team.owner.username == assignee:
                    obj = TeamTask(taskDetail=objTask,assignee=assignee,assigned=True)
                    obj.save()
                else:
                    obj = TeamTask(taskDetail=objTask,assignee=team.owner.username,assigned=False)
                    obj.save()
                print(i)
                return redirect('teamTask',team_id,title)
        else:
            message="User does not belong to the team!!!"
    return render(request,'create_team_task.html',{'team_id':team_id,'message':message})


def team__task_view(request,team_id,taskname):
    team=Team.objects.get(id=team_id)
    taskMembers=TaskDetail.objects.filter(team=team).filter(title=taskname)
    task = taskMembers[0]
    taskMembers = TeamTask.objects.filter(taskDetail=taskMembers[0])
    #print(len(taskMembers))
    return render(request,'task.html',{'taskMembers':taskMembers,'request':request,'id':team_id,'task':task})


def team_task_edit_view(request,team_id,taskname):
    message=""
    if request.method=='POST':
        team=Team.objects.get(id=team_id)
        title=request.POST.get('taskname')
        description=request.POST.get('description')
        exists=TaskDetail.objects.filter(team=team).filter(title=title)
        if len(exists)>0 and taskname!=title:
            message="You already have a task with that name!!!"
        else:
            objs=TaskDetail.objects.filter(team=team).filter(title=taskname)
            for obj in objs:
                obj.title=title
                obj.description=description
                obj.save()
            return redirect('teamTask',team_id,title)
    return render(request,'team_task_edit.html',{'message':message,'request':request,'id':team_id})

def team_task_modify_view(request,team_id,taskname):
    team=Team.objects.get(id=team_id)
    taskDetail = TaskDetail.objects.filter(team=team).get(title=taskname)
    teamMembers = TeamTask.objects.filter(taskDetail=taskDetail)
    if request.method=='POST':
        taskMemberIds=request.POST.getlist('list')
        taskMembers = TeamTask.objects.filter(taskDetail=taskDetail)
        for taskMember in taskMembers:
            taskMember.assigned=False
            taskMember.save()
        for taskMemberId in taskMemberIds:
            obj=TeamTask.objects.get(id=taskMemberId)
            obj.assigned = True
            obj.save()
        return redirect('teamTask',team_id,taskname)
    return render(request,'task_modify_members.html',{'teamMembers':teamMembers,'id':team_id,'taskname':taskname})
