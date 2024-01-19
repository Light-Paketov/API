from django.db import models
from django.core.validators import MaxValueValidator

class Gender(models.Model):
    title = models.CharField(max_length=7, unique=True, null=False)
    
    def __str__(self):
        return self.title

class User(models.Model):
    nickname = models.CharField(max_length=20, unique=True, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    full_name = models.CharField(max_length=70, null=False)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=False)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)], null=False) #Положительные числа с максимальным значением 100
    
    def __str__(self):
        return self.nickname
