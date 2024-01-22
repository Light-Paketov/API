from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Gender, User, Diet, Product

from django.contrib.auth.hashers import make_password

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['title']

class UserSerializer(serializers.ModelSerializer):
    #gender = GenderSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'gender', 'age']
        
        # Дополнительные параметры
        extra_kwargs = {
            'password': {'write_only': True},  #Пароль только для чтения
        }
    
    #Хеширование пароля
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(UserSerializer, self).create(validated_data)

        # Создаем токен
        Token.objects.create(user=user)

        return user
        
class DietSerializer(serializers.ModelSerializer):
    #author = UserSerializer()
    class Meta:
        model = Diet
        fields = ['title', 'author']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['diet', 'icon', 'category', 'title', 'description', 'calories', 'proteins', 'fats', 'carbohydrates', 'vitamins', 'price', 'weight']