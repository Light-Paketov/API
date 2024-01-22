from django.contrib import admin
from .models import Gender, User, Diet, Category, Vitamins, Product

class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        'nickname'
    ]
class DietModelAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]
    
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]
    
class VitaminsModelAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]
    
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]

admin.site.register(User, UserModelAdmin)
admin.site.register(Gender)
admin.site.register(Diet, DietModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Vitamins, VitaminsModelAdmin)
admin.site.register(Product, ProductModelAdmin)
