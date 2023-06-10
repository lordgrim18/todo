from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Task


class TaskForm(ModelForm):
	# title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new task...'}))

	class Meta:
		model = Task
		
		fields = '__all__'

		exclude = ['task_owner', 'created']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
