from django.shortcuts import render,redirect, get_object_or_404,Http404
from django.views.generic import CreateView
from .models import User, Project, Group, Deployment,Profile,File,Suggestion, Task, Todo, Application
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ChoiceForm
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from .forms import CreateProject,CreateFile,CreateSuggestion, CreateTask, CreateToDo, NewTask, CreateApplication
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from notifications.signals import notify
import copy
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
	return render(request, 'accounts/index.html')

def is_member(user):
    return user.groups.filter(name='Deployers').exists()
    
def files(request):
	return render(request,'accounts/files.html')

def home(request):
    projects_list = Project.objects.all()
    sugg = Suggestion.objects.filter(new_suggestion=True)
    suggestions = []
    apps = []
    task = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    for i in sugg:
        if i.file.project.deployer == request.user:
            suggestions.append(i)
    tasks = Task.objects.filter(new_task=True)
    for i in tasks:
        deps = i.deployers.all()
        if request.user in deps:
            task.append(i)
    context = {'projects_list': projects_list, 'suggestions':suggestions, 'task':task, 'apps':apps}
    if request.user.is_authenticated:
        return render(request, 'accounts/home.html', context)
    else:
        return redirect('/profiles/login/')

def signup(request):
    return render(request, 'signup.html')

def details(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    project = Project.objects.get(pk=project_id)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    taskslist = []
    initdate = []
    finishdate = []
    deployer = []
    workers = ''
    files = project.file_set.all()
    files_no = len(files)
    tasks = project.task_set.all()
    tasks_no = len(tasks)
    for task in project.task_set.all():
        taskslist.append(task.task_name)
        initdate.append(task.creation_date)
        finishdate.append(task.deadline)
        work = task.deployers.all()
        for i in work:
            workers +=  i.user.username + ' , '
        deployer.append(workers)
        workers = ''
    json1 = json.dumps(list(taskslist), cls=DjangoJSONEncoder)
    jsoninit = json.dumps(list(initdate), cls=DjangoJSONEncoder)
    jsonfinish = json.dumps(list(finishdate), cls=DjangoJSONEncoder)
    jsondep = json.dumps(list(deployer), cls=DjangoJSONEncoder)
    project.views += 1
    project.save()
    try: 
        workers = project.workers.all()
        workers_no = len(workers)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    if request.user.is_authenticated:
        return render(request, 'accounts/details.html', {'apps':apps, 't':t, 's':s, 'project': project, 'workers':workers, 'json1':json1, 'jsondep':jsondep ,'jsoninit':jsoninit, 'jsonfinish':jsonfinish, 'project':project, 'initdate':initdate, 'finishdate':finishdate, 'taskslist':taskslist, 'workers_no':workers_no, 'files_no':files_no, 'tasks_no':tasks_no})
    else:
        return redirect('/profiles/login/')    

def files(request, file_id, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)    
    try:
        files = File.objects.get(pk=file_id)
        f = open('%s' %files.file, 'r')
        content = f.read()
        f.close()
    except File.DoesNotExist:
        raise Http404("File does not exist")
    if request.user.is_authenticated:
        return render(request, 'accounts/files.html', {'t':t, 's':s,'files': files,'project':project,'content':content , 'apps':apps})
    else:
        return redirect('/profiles/login/')    
    

def v_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            content_type = ContentType.objects.get_for_model(Project)            
            perm1 = Permission.objects.get(
            codename='view_project',
            content_type=content_type,
            )
            profile = user.profile
            profile.username = user.username
            profile.save()
            user.user_permissions.add(perm1)
            login(request, user)
            return redirect('/home/')
    else:
        form = SignUpForm()
    return render(request, 'viewersignup.html', {'form': form})


def base(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    return render(request, 'accounts/base.html', {'t':t, 's':s, 'apps':apps})

def profile_deployments(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = request.user
    project = Project.objects.get(pk=project_id)
    profile = Profile.objects.get(user_id=user.id)
    profile.username = user.username
    if (is_member(user)) and (user==project.deployer) and (project.deployed==False):
        if profile:
            profile.no_deployments +=1
            project.deployed = True
        profile.save()
        project.save()
        return redirect("/home/%d" %project_id)
        return render(request, 'accounts/profdep.html', {'t':t, 's':s,'user':user,'project':project,'profile':profile, 'apps':apps})
    else:
        if (project.deployer != user):
            return HttpResponse("Permission denied!")
        elif (project.deployed==True):
            return HttpResponse("This Project is already marked as deployed!")        
        return HttpResponse("Pleas Login as a deployer!")

def successful(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    lst = []
    lstviewer = []
    result=[]
    ranking = []
    viewer_ranking = []
    deployments=Profile.objects.all()
    for profile in deployments:
        if is_member(profile.user):
            lst.append((profile.no_deployments,profile.user.username))
        else:
            if not(profile.user.is_superuser):
                lstviewer.append((profile.points,profile.user.username))
    succ = max(lst)
    ranking1 = sorted(lst,reverse=True)
    for i in ranking1:
        ranking.append(i[1])
    viewer_ranking1 = sorted(lstviewer, reverse=True)
    for j in viewer_ranking1:
        viewer_ranking.append(j[1])
    if request.user.is_authenticated:
        return render(request, 'accounts/successful.html', {'t':t, 's':s, 'deployments':deployments, 'lst':lst, 'succ':succ, 'result':result,'profile':profile,'ranking':ranking, 'viewer_ranking':viewer_ranking, 'apps':apps})
    else:
        return redirect('/profiles/login/')    



def create_project(request):
   apps = []
   app = Application.objects.filter(new_app=True)
   for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
   t = Task.objects.filter(new_task=True)
   s = Suggestion.objects.filter(new_suggestion=True)
   if request.method == "POST":
        form = CreateProject(request.POST)
        if form.is_valid():
            user = request.user
            if (is_member(user)):
                project= form.save(commit=False)
                project.deployer = request.user
                project.save()
                form.save_m2m()
                project.workers.add(request.user.profile)
                project.save()
                return redirect('/home/', pk=project.id)
            else:
                return HttpResponse("Permission denied!")
   else:
        form = CreateProject()
        return render(request, 'accounts/create_project.html', {'t':t, 's':s, 'form': form, 'apps':apps})



def edit_project(request,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = CreateProject(request.POST, instance=project)
        user = request.user
        if (is_member(user)) and (user==project.deployer):
            if form.is_valid():
                project = form.save(commit=False)
                project.deployer = request.user
                project.save()
                return redirect('/home/', pk=project.pk)
        else:
            return HttpResponse("Permission denied!")
    else:
        form = CreateProject(instance=project)
    return render(request, 'accounts/edit_project.html', {'t':t, 's':s, 'form': form, 'apps':apps})


def delete_project(request,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if (is_member(user)) and (user==project.deployer):
        form = CreateProject(request.POST, instance=project)
        project.delete()
        return render(request, 'accounts/deleted.html', {'t':t, 's':s, 'form': form, 'apps':apps})
    else:
        return HttpResponse("Permission denied!")

def deletef(request,file_id,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id)    
    return render(request,'accounts/deletef.html',{'t':t, 's':s, 'file': file,'project':project, 'apps':apps})

def deletep(request,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    return render(request,'accounts/deletep.html',{'t':t, 's':s, 'project':project, 'apps':apps})

def delete_file(request,file_id,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = get_object_or_404(Project,pk=project_id)
    user = request.user
    if (is_member(user)) and (user==project.deployer):
        file = get_object_or_404(File, pk=file_id)
        form = CreateFile(request.POST, instance=file)
        file.delete()
        return redirect("/home/%d" %project_id)    
        return render(request, 'accounts/deleted.html', {'t':t, 's':s, 'form': form,'project':project, 'apps':apps})
    else:
        return HttpResponse("Permission denied!")

def create_file(request,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    proje = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = CreateFile(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if (is_member(user)) and (user==proje.deployer):
                file= form.save(commit=False)
                file.project = proje
                file.deployer = request.user
                file.save()
                return redirect('/home/%d' %project_id, pk=file.id)
            else:
                return HttpResponse("Permission denied!")
    else:
        form = CreateFile()
    return render(request, 'accounts/create_file.html', {'t':t, 's':s, 'form': form,'proje':proje, 'apps':apps})   

def create_suggestion(request,project_id,file_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id)
    user = request.user
    profile = Profile.objects.get(user_id=user.id)    
    if request.method == "POST":
        form = CreateSuggestion(request.POST, request.FILES)
        if form.is_valid():
            sfile= form.save(commit=False)
            sfile.author=user
            sfile.file = file
            sfile.new_suggestion= True
            sfile.save()
            project.new_suggestion=True
            project.save()
            file.new_suggestion=True
            file.save()
            profile.points +=1
            profile.save()
            post_save.connect(my_handler, sender=user)
            notify.send(project.deployer, recipient=project.deployer, verb='you have one new suggestion on project %s' %project.project_name)
            return redirect('/home/%d/%d/viewsuggestions/%d/' % (project_id ,file_id, sfile.id))
    else:
        form = CreateSuggestion()
    return render(request, 'accounts/create_suggestion.html', {'t':t, 's':s, 'form': form,'project':project,'file':file, 'apps':apps})   

def view_suggestions(request,project_id,file_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    try:
        file = File.objects.get(pk=file_id)
        if request.user == project.deployer:
            file.new_suggestion=False
            file.save()
    except File.DoesNotExist:
        raise Http404("File does not exist")
    return render(request, 'accounts/view_suggestions.html', {'t':t, 's':s, 'project': project,'file':file, 'apps':apps})

def suggestions(request,project_id,file_id,suggestion_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id)  
    try:
        suggestions = Suggestion.objects.get(pk=suggestion_id)
        f = open('%s' %suggestions.sfile, 'r')
        content = f.read()
        f.close()
    except Suggestion.DoesNotExist:
        raise Http404("File does not exist")
    return render(request, 'accounts/suggestions.html', {'t':t, 's':s, 'file': file,'project':project,'suggestions':suggestions,'content':content, 'apps':apps})

def confirm_suggestion(request,project_id,file_id,suggestion_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id) 

    try:
        suggestions = Suggestion.objects.get(pk=suggestion_id)
    except Suggestion.DoesNotExist:
        raise Http404("File does not exist")
    if request.user == project.deployer:
        if suggestions.confirmed == True:
            return HttpResponse("This suggestion is already confirmed!")
        else:
            suggestions.confirmed = True
            profile = suggestions.author.profile
            profile.points +=1
            file.file = suggestions.sfile
            file.suggestions = False
            file.save()
            profile.save()
            suggestions.save()
            return render(request, 'accounts/confirm_suggestion.html',{'t':t, 's':s, 'file': file,'project':project,'suggestions':suggestions, 'apps':apps})
    else:
        return HttpResponse("Permission denied!")

def myprojects(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = request.user
    if request.user.is_authenticated:
        return render(request, 'accounts/myprojects.html', {'t':t, 's':s, 'user':user, 'apps':apps})
    else:
        return redirect('/profiles/login/')   

def accepting_sugg(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    projects = Project.objects.all()
    if request.user.is_authenticated:
        return render(request, 'accounts/accepting_sugg.html', {'t':t, 's':s, 'projects':projects, 'apps':apps})
    else:
        return redirect('/profiles/login/')  


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was saved')

def notifications(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    suggestions = Suggestion.objects.filter(new_suggestion=True)
    task = Task.objects.filter(new_task=True)
    apps = Application.objects.filter(new_app=True)
    user = request.user
    if is_member(user):
        for sugg in suggestions:
            sugg.new_suggestion=False
            sugg.save()
        for i in task:
            i.new_task= False
            i.save()
        for i in apps:
            i.new_app = False
            i.save()
    user.notifications.mark_all_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/notifications.html', {'t':t, 's':s, 'projects':projects, 'tasks':tasks, 'task':task, 'apps':apps}) 
  

def profiles(request, name):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = User.objects.get(username=name)
    tasks = Task.objects.all()
    taskslist = []
    for task in tasks:
        deps = task.deployers.all()
        if user.profile in deps:
            taskslist.append(task)
    return render(request, 'accounts/profiles.html', {'t':t, 's':s, 'user':user, 'taskslist':taskslist, 'apps':apps})

def confirm_request(request,name):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = User.objects.get(username=name)
    post_save.connect(my_handler, sender=user)
    notify.send(user, recipient=user, verb='you have one new request')
    user.profile.notification = True
    user.save()
    return render(request, 'accounts/confirm_request.html', {'t':t, 's':s, 'user':user, 'apps':apps})

def request(request, name):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = User.objects.get(username=name)
    return render(request, 'accounts/request.html', {'t':t, 's':s, 'user':user, 'apps':apps})


def deployer_confirm(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    user = request.user
    my_group = Group.objects.get(name='Deployers') 
    my_group.user_set.add(user) 
    return render(request,'accounts/deployer.html', {'t':t, 's':s, 'user':user, 'apps':apps})

def find_deployer(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    users = User.objects.all()
    projects = Project.objects.all()
    return render(request, 'accounts/find_deployer.html', {'t':t, 's':s, 'users':users,'projects':projects, 'apps':apps})  
      
def subject(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    return render(request, 'accounts/subject.html', {'t':t, 's':s, 'subject':subject, 'apps':apps})

def update(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    vers = []
    lst = Project.objects.filter(project_name=project.project_name)
    for i in lst:
        vers.append(i.version)
    version = max(vers)
    if project.updated == False and project.deployed == True:
        files = project.file_set.all()
        project1 = Project()
        project1.project_name = project.project_name
        project1.deployer = project.deployer
        project1.version = version + 1
        lst = []
        project1.save()
        for i in files:
            j = copy.deepcopy(i)
            lst.append(j)
        for file in lst:
            project1.file_set.create(file_name=file.file_name,file=file.file)
            project1.save()
    else:
        return HttpResponse("This project is not finished or is already updated!")
    project.updated = True
    project.save()
    return redirect("/home/%d" %project1.id)
    return render(request, 'accounts/update.html', {'t':t, 's':s, 'project1':project1, 'lst':lst, 'apps':apps})

def history(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    return render(request, 'accounts/history.html', {'t':t, 's':s, 'project':project, 'apps':apps})

def goback(request,project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    project1 = Project.objects.get(project_name=project.project_name, updated=False)
    project.updated=False
    project1.updated=True
    project1.save()
    project.save()
    return redirect("/home/%d" %project_id)
    return render(request, 'accounts/goback.html', {'t':t, 's':s, 'project':project, 'apps':apps})

def graph(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    #Step 1: Create a DataPool with the data we want to retrieve.
    data = \
        DataPool(
           series=
            [{'options': {
               'source': Profile.objects.all()},
              'terms': [
                'username',
                'no_deployments',
                'tasks', 
                'points']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'username': [
                    'no_deployments', 
                    'tasks',
                    'points']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Deployments data'},
               'xAxis': {
                    'title': {
                       'text': 'users'}}})
    #Step 3: Send the chart object to the template.
    return render(request, 'accounts/graph.html', {'t':t, 's':s, 'graph': cht, 'apps':apps})

def create_task(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    day = 600
    user = request.user
    if(user.is_superuser or user == project.deployer):
        if request.method == "POST":
            form = CreateTask(request.POST)
            if form.is_valid():
                task= form.save(commit=False)
                task.project = project
                task.creation_date = timezone.now()
                project.alltasks += 1
                project.progress = project.finished_tasks*100/project.alltasks
                task.new_task = True
                task.save()
                form.save_m2m()
                task.deployers.add(project.deployer.profile)
                deps = task.deployers.all()
                diff = task.deadline-task.creation_date
                task.budget = len(deps)*600*diff.days
                project.budget += task.budget
                project.save()
                task.save()
                return redirect('%d/next/' %task.id)
        else:
            form = CreateTask()
        project.new_task = True
        project.save()
    return render(request, 'accounts/tasks.html', {'t':t, 's':s, 'form':form, 'apps':apps})

def create_task1(request,project_id, task_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    day=600
    task1 = Task.objects.get(pk=task_id)
    url = task_id
    profiles = Profile.objects.filter(skills=task1.subject)
    for i in profiles:
        i.search = True
        i.save()
    project = get_object_or_404(Project, pk=project_id)
    form = NewTask(request.POST)
    user = request.user
    if(user.is_superuser or user == project.deployer):
        if request.method == "POST":
            form = NewTask(request.POST)
            if form.is_valid():
                task= form.save(commit=False)
                task.task_name = task1.task_name
                task.subject = task1.subject
                task.description = task1.description
                task.project = task1.project
                task.deadline = task1.deadline
                task.creation_date = timezone.now()
                task.new_task = True
                task.save()
                form.save_m2m()
                task.deployers.add(project.deployer.profile)
                task.budget = task1.budget
                task.save()
                deps = task.deployers.all()
                for i in deps:
                    i.unfinished_tasks += 1
                    diff = task.deadline-task.creation_date
                    i.payment += diff.days * day
                    diff=0
                    i.save()
                    dep = User.objects.get(username=i.username)
                    post_save.connect(my_handler, sender=user)
                    notify.send(dep, recipient=dep, verb='you have new tasks to complete %s' %project.project_name)
                    dep = User()
                return redirect('/home/%d/createtask/%d/next/1/' %(project_id, task_id))
        else:
            form = NewTask()
    return render(request, 'accounts/create_task1.html', {'t':t, 's':s, 'profiles':profiles, 'form':form, 'url':url, 'apps':apps})

def create_task2(request,project_id, task_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    task = Task.objects.get(pk=task_id)
    profiles = Profile.objects.filter(skills=task.subject)
    for i in profiles:
        i.search = False
        i.save()
    task.delete()
    return redirect('/home/%d/tasks/%d/' %(project_id, task_id+1))
    return render(request, 'accounts/create_task2.html', {'t':t, 's':s, 'apps':apps})


def tasks(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    taskslist = project.task_set.all()
    return redirect('/home/%d' %project_id)
    return render(request, 'accounts/taskslist.html', {'t':t, 's':s, 'taskslist':taskslist, 'apps':apps})

def taskdetails(request, project_id, task_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    return render(request, 'accounts/taskdetails.html', {'t':t, 's':s, 'task':task, 'project':project, 'apps':apps})

def alltasks(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    taskslist = []
    initdate = []
    finishdate = []
    deployer = []
    for task in project.task_set.all():
        if task.finished == True:
            taskslist.append(task.task_name + "- COMPLTED")
        else:
            taskslist.append(task.task_name + "- NOT COMPLTED")
        initdate.append(task.creation_date)
        work = task.deployers.all()
        for i in work:
            workers +=  i.user.username + ' , '
        deployer.append(workers)
        workers = ''
        deployer.append(task.project.deployer.username)
    json1 = json.dumps(list(taskslist), cls=DjangoJSONEncoder)
    jsoninit = json.dumps(list(initdate), cls=DjangoJSONEncoder)
    jsonfinish = json.dumps(list(finishdate), cls=DjangoJSONEncoder)
    jsondep = json.dumps(list(deployer), cls=DjangoJSONEncoder)
    return render(request, 'accounts/alltasks.html', {'t':t, 's':s, 'json1':json1, 'jsondep':jsondep ,'jsoninit':jsoninit, 'jsonfinish':jsonfinish, 'project':project, 'initdate':initdate, 'finishdate':finishdate, 'apps':apps})

def finish_task(request, project_id, task_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    if (request.user == project.deployer or request.user.is_superuser):
        task.finished=True
        task.finishtime = timezone.now()
        project.finished_tasks += 1
        project.progress = project.finished_tasks*100/project.alltasks
        project.save()
        task.save()
        user = request.user.profile
        user.tasks += 1
        user.save()
        for deployer in task.deployers.all():
            deployer.finished_tasks += 1
            deployer.unfinished_tasks -= 1
            deployer.save()
        if task.finished == True:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/finishtask.html', {'t':t, 's':s, 'apps':apps})

def maintasks(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    taskslist = []
    initdate = []
    finishdate = []
    deployer = []
    workers = ''
    taskslist1 = Task.objects.all()
    for task in taskslist1:
        if task.finished == True:
            taskslist.append(task.task_name + "- COMPLTED")
        else:
            taskslist.append(task.task_name + "- NOT COMPLTED")
        initdate.append(task.creation_date)
        finishdate.append(task.deadline)
        work = task.deployers.all()
        for i in work:
            workers +=  i.user.username + ' , '
        deployer.append(workers)
        workers = ''
    json1 = json.dumps(list(taskslist), cls=DjangoJSONEncoder)
    jsoninit = json.dumps(list(initdate), cls=DjangoJSONEncoder)
    jsonfinish = json.dumps(list(finishdate), cls=DjangoJSONEncoder)
    jsondep = json.dumps(list(deployer), cls=DjangoJSONEncoder)
    return render(request, 'accounts/maintasks.html', {'json1':json1, 'jsondep':jsondep ,'jsoninit':jsoninit, 'jsonfinish':jsonfinish, 'initdate':initdate, 'finishdate':finishdate, 'apps':apps})

def add_deployers(request, project_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    profiles = User.objects.all()
    project = Project.objects.get(pk=project_id)
    workers = project.workers.all()    
    return render(request, 'accounts/add_deployers.html', {'t':t, 's':s, 'profiles':profiles, 'workers':workers, 'project':project, 'apps':apps})

def add(request, project_id, name):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    profiles = User.objects.all()
    project = Project.objects.get(pk=project_id)
    deployer = User.objects.get(username=name)
    project.workers.add(deployer.profile)
    return render(request, 'accounts/add.html', {'t':t, 's':s, 'profiles':profiles, 'deployer':deployer, 'apps':apps})

def tasks1(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    taskslist = [[]]
    initdate = [[]]
    finishdate = [[]]
    deployer = []
    taskslst = []
    initdt = []
    finishdt = []
    deployerslist = Profile.objects.all()
    tasks = Task.objects.all()
    workers = ''
    for i in deployerslist:
        deployer.append(i.username)
        for task in tasks:
            deps = task.deployers.all()
            if i in deps:
                taskslst.append(task.task_name)
                initdt.append(task.creation_date)
                finishdt.append(task.deadline)
        taskslist.append(taskslst)
        initdate.append(initdt)
        finishdate.append(finishdt)
        taskslst=[]
        initdt=[]
        finishdt=[]
    json1 = json.dumps(list(taskslist), cls=DjangoJSONEncoder)
    jsoninit = json.dumps(list(initdate), cls=DjangoJSONEncoder)
    jsonfinish = json.dumps(list(finishdate), cls=DjangoJSONEncoder)
    jsondep = json.dumps(list(deployer), cls=DjangoJSONEncoder)
    return render(request, 'accounts/task1.html', {'t':t, 's':s, 'json1':json1, 'jsondep':jsondep ,'jsoninit':jsoninit, 'jsonfinish':jsonfinish, 'initdate':initdate, 'finishdate':finishdate, 'apps':apps})


def profs(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    profiles = Profile.objects.all()
    return render(request, 'accounts/profs.html', {'t':t, 's':s, 'profiles':profiles, 'apps':apps})

def pay(request, name):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    profile = Profile.objects.get(username=name)
    profile.total_payment += profile.payment
    profile.payment = 0
    profile.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, "accounts/payment.html", {'t':t, 's':s, 'apps':apps})

def create_todo(request,project_id, task_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    task = Task.objects.get(pk=task_id)
    proje = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = CreateToDo(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if (user.is_superuser  ) or (user==proje.deployer):
                todo= form.save(commit=False)
                todo.task = task
                todo.save()
                return redirect('/home/%d' %project_id, pk=todo.id)
            else:
                return HttpResponse("Permission denied!")
    else:
        form = CreateToDo()
    task.to_dos += 1
    task.progress = task.finished_todos*100/task.to_dos
    task.save()
    return render(request, 'accounts/create_todo.html', {'t':t, 's':s, 'form': form,'proje':proje, 'apps':apps})   

def todo_details(request, project_id, task_id, todo_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    todo = Todo.objects.get(pk=todo_id)
    return render(request, 'accounts/todo_details.html', {'t':t, 's':s, 'todo':todo, 'apps':apps})

def todo_finish(request, project_id, task_id, todo_id):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    todo = Todo.objects.get(pk=todo_id)
    todo.completed = True
    task = Task.objects.get(pk=task_id)
    task.finished_todos += 1
    task.progress = task.finished_todos*100/task.to_dos
    todo.save()
    task.save()
    project = Project.objects.get(pk=project_id)
    if(todo.completed):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/todo_finish.html', {'t':t, 's':s, 'apps':apps})

def jobs(request):
    apps = []
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    tasks1 = Task.objects.all()
    tasks = []
    for task in tasks1:
        if task.job == True:
            tasks.append(task)
    return render(request, 'accounts/jobs.html', {'t':t, 's':s, 'tasks':tasks, 'apps':apps})

def create_job(request, task_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    task = Task.objects.get(pk=task_id)
    task.job = True
    task.save()
    return render(request, 'accounts/create_job.html', {'t':t, 's':s, 'task':task, 'apps':apps})

def apply(request, task_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    task = Task.objects.get(pk=task_id)
    user = request.user
    if(user.is_authenticated):
        if request.method == "POST":
            form = CreateApplication(request.POST)
            if form.is_valid():
                reason= form.save(commit=False)
                reason.task = task
                reason.profile = user.profile
                reason.new_app = True
                reason.save()
                task.applications += 1
                task.save()
                post_save.connect(my_handler, sender=user)
                notify.send(task.project.deployer, recipient=task.project.deployer, verb='you have one new application ')
                return redirect('/jobs/')
        else:
            form = CreateApplication()

        return render(request, 'accounts/apply.html', {'t':t, 's':s, 'task':task, 'form':form, 'apps':apps})
    else:
        return redirect('/profiles/login')

def view_applications(request, task_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    task = Task.objects.get(pk=task_id)
    app = task.application_set.all()
    return render(request, 'accounts/apps.html', {'t':t, 's':s, 'task':task, 'app':app, 'apps':apps})

def accept(request,task_id ,application_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    task = Task.objects.get(pk=task_id)
    appl = Application.objects.get(pk=application_id)
    task.deployers.add(appl.profile)
    task.save()
    appl.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/accept.html', {'t':t, 's':s, 'apps':apps})

def decline(request, application_id, task_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    task = Task.objects.get(pk=task_id)
    appl = Application.objects.get(pk=application_id)
    appl.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/decline.html', {'t':t, 's':s, 'apps':apps})

def remove_job(request, task_id, project_id):
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    task.job = False
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/remove_job.html', {'t':t, 's':s, 'task':task, 'apps':apps})

def mytasks(request):
    apps = []
    app = Application.objects.filter(new_app=True)
    for j in app:
        if request.user == j.task.project.deployer:
            apps.append(j)
    t = Task.objects.filter(new_task=True)
    s = Suggestion.objects.filter(new_suggestion=True)
    taskslist = []
    taskslist1=[]
    initdate = []
    finishdate = []
    deployer = []
    workers = ''
    ts = Task.objects.all()
    for j in ts:
        deps = j.deployers.all()
        if request.user.profile in deps:
            taskslist1.append(j)
    for task in taskslist1:
        if task.finished == True:
            taskslist.append(task.task_name + "- COMPLTED")
        else:
            taskslist.append(task.task_name + "- NOT COMPLTED")
        initdate.append(task.creation_date)
        finishdate.append(task.deadline)
        work = task.deployers.all()
        for i in work:
            workers +=  i.user.username + ' , '
        deployer.append(workers)
        workers = ''
    json1 = json.dumps(list(taskslist), cls=DjangoJSONEncoder)
    jsoninit = json.dumps(list(initdate), cls=DjangoJSONEncoder)
    jsonfinish = json.dumps(list(finishdate), cls=DjangoJSONEncoder)
    jsondep = json.dumps(list(deployer), cls=DjangoJSONEncoder)
    return render(request, 'accounts/mytasks.html', {'taskslist1':taskslist1 ,'json1':json1, 'jsondep':jsondep ,'jsoninit':jsoninit, 'jsonfinish':jsonfinish, 'initdate':initdate, 'finishdate':finishdate, 'apps':apps})

def sugg(request, project_id, file_id):
    project = Project.objects.get(pk=project_id)
    file = File.objects.get(pk=file_id)
    file.suggestions = True
    file.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'accounts/sugg.html', {})