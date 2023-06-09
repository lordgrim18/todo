from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(ModelForm):
	# title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new task...'}))

	class Meta:
		model = Task
		fields = '__all__'

		exclude = ['task_owner', 'created','complete']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
