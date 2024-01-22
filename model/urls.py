from django.urls import path

from .views import UsersView, UserView, DietsView, DietView, ProductsView, ProductView
app_name = "model"

#model.User
urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:firstID>', UserView.as_view()),
    path('user/<int:firstID>-<int:lastID>', UserView.as_view())
]

#models.Diet
urlpatterns += [
    path('diets/', DietsView.as_view(), name='diets'),
    path('diet/<int:firstID>', DietView.as_view()),
    path('diet/<int:firstID>-<int:lastID>', DietView.as_view())
]

#model.Product
urlpatterns += [
    path('products/', ProductsView.as_view(), name='products'),
    path('product/<int:firstID>', ProductView.as_view()),
    path('product/<int:firstID>-<int:lastID>', ProductView.as_view())
]