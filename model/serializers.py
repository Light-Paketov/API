from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Gender, User, Diet, Product, Ingestion, Category, Vitamins

from django.contrib.auth.hashers import make_password

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['title']

class UserSerializer(serializers.ModelSerializer):
    #gender = GenderSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'gender']

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
        fields = ['id', 'title', 'author']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['author','diet', 'category', 'title', 'description', 'calories', 'proteins', 'fats', 'carbohydrates', 'vitamins', 'price', 'weight']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class VitaminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitamins
        fields = ['id', 'title']

class IngestionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    remove_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, many=True)

    class Meta:
        model = Ingestion
        fields = ['product', 'remove_product']

    def update(self, instance, validated_data):
        instance.product.add(*validated_data.get('product', []))
        instance.product.remove(*validated_data.get('remove_product', []))

        return instance
