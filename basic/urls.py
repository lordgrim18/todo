from django.urls import path
from . import views


urlpatterns = [
     path('',views.home, name="home"),

    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),

    path('profile/<str:pk>',views.userProfile, name='profile'),
    path('update-user/',views.updateUser, name='update-profile'),

    path('create-task/',views.createTask, name='create-task'),
    path('update-task/<str:pk>',views.updateTask, name='update-task'),
    path('delete-task/<str:pk>',views.deleteTask, name='delete'),
    path('change-status/<str:pk>' , views.change_task_status, name='change-status' ), 

    path('due-tomorrow/',views.dueTomorrow, name='due-tomorrow'),
    path('due-this-week/',views.dueThisWeek, name='due-this-week'),
    path('due-this-month/',views.dueThisMonth, name='due-this-month'),

]