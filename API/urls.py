from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from model.views import all_models

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', all_models),
    path('api/', include('model.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


