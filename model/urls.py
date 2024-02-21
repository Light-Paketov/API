from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import UsersView, LoginView, DietsView, CategoriesView, VitaminesView, ProductsView, IngestionView
app_name = "model"

#Auth
urlpatterns = [
    path('auth-signup', UsersView.as_view(), name='auth-signup'),
    path('auth-login', LoginView.as_view(), name='auth-login'),
    path('token-refresh', TokenRefreshView.as_view)
]

#models.Diet
urlpatterns += [
    path('dietes/token:<str:token>/', DietsView.as_view(), name='dietes-list'),
    path('diet:<str:title>/token:<str:token>/', DietsView.as_view(), name='diets-user'),
]

#model.Category
urlpatterns += [
    path('categories/', CategoriesView.as_view(), name='categories-list'),
]

#model.Vitamines
urlpatterns += [
    path('vitamines/', VitaminesView.as_view(), name='vitamines-list'),
]

# #model.Product
urlpatterns += [
    path('products/token:<str:token>/', ProductsView.as_view(), name='products-list-user'),
    path('products/diet:<str:dietTitle>/token:<str:token>', ProductsView.as_view()),
    path('products/diet:<str:dietTitle>/ingestion:<str:ingestionTitle>,token:<str:token>', ProductsView.as_view()),
    path('product:<str:productTitle>/token:<str:token>', ProductsView.as_view(), name='update_product')
]

#model.Ingestion
urlpatterns += [
    path('diet:<str:diet>/ingestion:<str:title>', IngestionView.as_view()),
]