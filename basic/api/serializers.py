from rest_framework import serializers  
from rest_framework.serializers import ModelSerializer
from basic.models import Task


class TaskSerializer(ModelSerializer):


    class Meta:
        model = Task
        fields = (
            'id','task_owner','title','deadline','complete'
        )
        
