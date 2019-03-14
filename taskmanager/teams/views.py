
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .models import User,Team,AllUser

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
    # print(myTeams)
    # print(memberTeams)

    return render(request,'teamstasks_list.html',{'myTeams':myTeams,'memberTeamName':memberTeamName})

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
    return render(request,'team.html',{'message':message,'id':pk,'members':members,'flag':flag,'ownerUserName':ownerUserName,'request':request})

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


def create_task_view(request):
    message=""
    if request.method=='POST':
