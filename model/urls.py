from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UsersView, UserView, LoginView, DietsView, DietView, ProductsView, ProductView, ProductDietView, ProductCategoryView, ProductIngestionView, ProductIngestionCategoryView
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

#model.Product.{Что-то}
urlpatterns += [
    path('products/diet:<str:diet>', ProductDietView.as_view()),
    path('products/diet:<str:diet>/category:<str:category>', ProductCategoryView.as_view()), #Diet может быть Null, т.e "products/diet:'Null'/category:<str:category>"
    path('products/diet:<str:diet>/ingestion:<str:ingestion>', ProductIngestionView.as_view()),
    path('products/diet:<str:diet>/ingestion:<str:ingestion>/category:<str:category>', ProductIngestionCategoryView.as_view()),   
]