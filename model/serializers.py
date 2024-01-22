from rest_framework import serializers
from .models import Gender, User, Diet, Product

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['title']

class UserSerializer(serializers.ModelSerializer):
    #gender = GenderSerializer()
    class Meta:
        model = User
        fields = ['nickname', 'email', 'password', 'full_name', 'gender', 'age']
        
        # Дополнительные параметры
        extra_kwargs = {
            'password': {'write_only': True},  #Пароль только для чтения
        }
        
class DietSerializer(serializers.ModelSerializer):
    #author = UserSerializer()
    class Meta:
        model = Diet
        fields = ['title', 'author']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['diet', 'icon', 'category', 'title', 'description', 'calories', 'proteins', 'fats', 'carbohydrates', 'vitamins', 'price', 'weight']