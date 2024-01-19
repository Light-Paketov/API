from django.urls import path

from .views import UsersView, UserView
app_name = "model"

#model.User
urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:firstID>', UserView.as_view()),
    path('user/<int:firstID>-<int:lastID>', UserView.as_view())
]