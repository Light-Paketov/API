from django.contrib import admin
from django.urls import path, include

from model.views import all_models

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', all_models),
    path('api/', include('model.urls')),
]


