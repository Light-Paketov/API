from django.db import models
from django.contrib.auth.models import AbstractUser

class Gender(models.Model):
    title = models.CharField(max_length=7, unique=True, null=False)

    def __str__(self):
        return self.title

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    full_name = models.CharField(max_length=70, null=False)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=False)
    # age = models.PositiveIntegerField(validators=[MaxValueValidator(100)], null=False) #Положительные числа с максимальным значением 100

    def __str__(self):
        return self.username

class Diet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=30, unique=True, null=False)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class Vitamins(models.Model):
    title = models.CharField(max_length=30, unique=True, null=False)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    diet = models.ManyToManyField(Diet)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)
    calories = models.FloatField(null=False)
    proteins = models.FloatField(null=False)
    fats  = models.FloatField(null=False)
    carbohydrates = models.FloatField(null=False)
    vitamins = models.ManyToManyField(Vitamins)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=None)
    weight = models.FloatField(null=False)

    def __str__(self):
        return self.title

class Ingestion(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=10)
    product = models.ManyToManyField(Product, null=True)

    def __str__(self):
        return self.title