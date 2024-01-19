from django.contrib import admin
from .models import Gender, User

class UserModelAdmin(admin.ModelAdmin):
    list_display=[
        'nickname'
    ]

admin.site.register(User, UserModelAdmin)
admin.site.register(Gender)
