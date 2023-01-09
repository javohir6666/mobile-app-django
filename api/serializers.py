from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields ='__all__'
    