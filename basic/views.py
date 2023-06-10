from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm, UserForm
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(task_owner = user)
        tasks_count = Task.objects.filter(task_owner = user, complete=False).count()

        completed_tasks = Task.objects.filter(task_owner = user, complete=True)
        current_datetime = timezone.now()
        pending_tasks = Task.objects.filter(task_owner = user, complete=False, deadline__gt=current_datetime)
        pending_tasks_count = pending_tasks.count()
        overdue_tasks = Task.objects.filter(task_owner = user, complete=False, deadline__lt=current_datetime)
        overdue_tasks_count = overdue_tasks.count()

        context = {'tasks':tasks, 'tasks_count':tasks_count, 'completed_tasks':completed_tasks,                         'pending_tasks':pending_tasks, 'overdue_tasks':overdue_tasks, 'pending_tasks_count':pending_tasks_count, 'overdue_tasks_count':overdue_tasks_count}
       
        return render(request, 'basic/home.html', context)
    else:
        return render(request, 'basic/home.html')


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')     #instead of home go back to the previous page???
        else:
            messages.error(request, 'username or password  does not exist')

    context = {'page':page}
    return render(request, 'basic/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occured')

    return render(request, 'basic/login_register.html', {'form': form})

@login_required(login_url='login')
def userProfile(request,pk):
    user = User.objects.get(id=pk)

    context = {'user':user}
    return render(request, 'basic/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'basic/update-user.html', {'form': form})

@login_required(login_url='login')
def createTask(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_owner = request.user
            task.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'basic/task_form.html', context)

@login_required(login_url='login')
def updateTask(request,pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.user != task.task_owner:
        return HttpResponse("you arent allowed here!!!")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home') 

    context = {'form': form}
    return render(request, 'basic/task_form.html', context)

@login_required(login_url='login')
def change_task_status(request,pk):
    task = Task.objects.get(id=pk)
    task.complete = not task.complete
    task.save()
    return redirect('home')

@login_required(login_url='login')
def deleteTask(request,pk):
    task = Task.objects.get(id=pk)

    if request.user != task.task_owner:
        return HttpResponse("you arent allowed here!!!!!!")
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    
    context = {'task': task}
    return render(request, 'basic/delete.html', context)

@login_required(login_url='login')
def dueTomorrow(request):
    user = request.user
    
    current_datetime = timezone.now()
    tomorrow = current_datetime + timedelta(days=1)
    pending_tasks = Task.objects.filter(task_owner = user, complete=False, deadline=tomorrow)
    pending_tasks_count = pending_tasks.count()

    context = {'pending_tasks':pending_tasks, 'pending_tasks_count':pending_tasks_count, 'next':tomorrow}
   
    return render(request, 'basic/due_next.html', context)

@login_required(login_url='login')
def dueThisWeek(request):
    user = request.user
    current_datetime = timezone.now()
    week = current_datetime + timedelta(days=7)
    pending_tasks = Task.objects.filter(task_owner = user, complete=False, deadline__lt=week, deadline__gt=current_datetime)
    pending_tasks_count = pending_tasks.count()

    context = {'pending_tasks':pending_tasks, 'pending_tasks_count':pending_tasks_count, 'next':week}

    return render(request, 'basic/due_next.html', context)

@login_required(login_url='login')
def dueThisMonth(request):
    user = request.user
    current_datetime = timezone.now()
    month = current_datetime + timedelta(days=30)
    pending_tasks = Task.objects.filter(task_owner = user, complete=False, deadline__lt=month, deadline__gt=current_datetime)
    pending_tasks_count = pending_tasks.count()

    context = {'pending_tasks':pending_tasks, 'pending_tasks_count':pending_tasks_count, 'next':month}
   
    return render(request, 'basic/due_next.html', context)
