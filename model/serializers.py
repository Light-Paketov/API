from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'password', 'full_name', 'gender', 'age']
        
        # Дополнительные параметры
        extra_kwargs = {
            'password': {'write_only': True},  #Пароль только для чтения
        }