from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UsersView, UserView, LoginView, DietsView, DietView, ProductsView, ProductView
app_name = "model"

#model.User
urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:firstID>', UserView.as_view()),
    path('user/<int:firstID>-<int:lastID>', UserView.as_view()),
]

#Auth
urlpatterns += [
    path('auth-signup', TokenObtainPairView.as_view(), name='auth-signup'),
    path('auth-login', LoginView.as_view(), name='auth-login'),
    path('token-refresh', TokenRefreshView.as_view)
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