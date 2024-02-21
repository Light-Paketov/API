from django.contrib.auth import authenticate

from .models import User, Diet, Category, Product, Ingestion, Vitamins
from .serializers import UserSerializer, DietSerializer, ProductSerializer, CategorySerializer, VitaminsSerializer, IngestionSerializer

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView

from .functions import get_user_by_token

class UsersView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response({"Users": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"User created": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

class DietsView(ListCreateAPIView):
    serializer_class =  DietSerializer
 
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', None) 
        user = get_user_by_token(token)
        if not user:
            return Response({f"Ошибка авторизации: Токен:{token} не найден"})
        title = kwargs.get('title', None)
        if not title:
                diets = Diet.objects.filter(author=user)
                if diets.count() == 0:
                    return Response({f"У {user} нет диет"})
                serializer = self.serializer_class(diets, many=True)
                return Response({f"Диеты пользователя {user}": serializer.data})
        else: 
            diet = Diet.objects.get(title=title)
            serializer = self.serializer_class(diet)
            return Response({f"Диета {diet.title} пользователя {user}": serializer.data})
        
    def post(self, request, *args, **kwargs):
        token = kwargs.get('token', None) 
        user = get_user_by_token(token)
        if not user:
            return Response({f"Ошибка авторизации: Токен:{token} не найден"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                author_username = User.objects.get(pk=serializer.data.get('author')).username
            except (User.DoesNotExist, TypeError):
                author_username = 'Unknown'
            return Response({f"Диета {serializer.data.get('title','Unknown')}, Автор:{author_username}": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"Categories": serializer.data})

class VitaminesView(APIView):
    def get(self, request):
        vitamines = Vitamins.objects.all()
        serializer = VitaminsSerializer(vitamines, many=True)
        return Response({"Vitamines": serializer.data})

class ProductsView(RetrieveUpdateDestroyAPIView):
    serializer_class =  ProductSerializer

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', None)
        user = get_user_by_token(token)
        if not user:
            return Response({"error": f"Ошибка авторизации: Токен:{token} не найден"})

        product_title = kwargs.get('productTitle', None)
        if not product_title:
            diet_title = kwargs.get('dietTitle', None)
            ingestion_title = kwargs.get('ingestionTitle', None)
            
            products = Product.objects.filter(author=user)
            if diet_title:
                products = products.filter(diet__title=diet_title)
            if ingestion_title:
                products = products.filter(ingestion__title=ingestion_title)

            if products.count() == 0:
                return Response({"error": f"Продукты не найдены"})
            serializer = self.serializer_class(products, many=True)
            return Response({"Продукты": serializer.data})
        else:
            product = Product.objects.filter(author=user, title=product_title).first()
            if not product:
                return Response({"error": "Продукт не найден или у пользователя нет доступа"})
            
            serializer = self.serializer_class(product)
            return Response({"Продукт": serializer.data})
        
    def post(self, request, *args, **kwargs):
        token = kwargs.get('token', None)  
        user = get_user_by_token(token)
        if not user:
            return Response({f"Ошибка авторизации: Токен:{token} не найден"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                author_username = User.objects.get(pk=serializer.data.get('author')).username
            except (User.DoesNotExist, TypeError):
                author_username = 'Unknown'
            return Response({f"Продукт {serializer.data.get('title','Unknown')}, Автор:{author_username}": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        token = kwargs.get('token', None)  
        user = get_user_by_token(token)
        if not user:
            return Response({f"Ошибка авторизации: Токен:{token} не найден"})
        title = kwargs.get('title', None)
        if not title:
            return Response({f"Ошибка: Метод PUT не поддерживает множество значений"})
        try:
            product = Product.objects.get(author=user, title=title)
            serializer = self.get_serializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f"Продукт обновлён": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": f"Продукт пользователя не найден или у нет разрешения на обновление"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        token = kwargs.get('token', None)  
        user = get_user_by_token(token)
        if not user:
            return Response({f"Ошибка авторизации: Токен:{token} не найден"})
        title = kwargs.get('title', None)
        if not title:
            return Response({f"Ошибка: Метод PUT не поддерживает множество значений"})
        try:
            product = Product.objects.get(author=user, title=title)
            product.delete()
            return Response({f"Продукт удалён": "success"})
        except User.DoesNotExist:
            return Response({f"Продукт": "not fount"}, status=status.HTTP_404_NOT_FOUND)
               
class IngestionView(UpdateAPIView):
    serializer_class = IngestionSerializer
    queryset = Ingestion.objects.all()
    lookup_field = 'title'

    def put(self, request, *args, **kwargs):
        title = kwargs.get("title", None)
        if not title:
            return Response({"error": "Method PUT not allowed. Title parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ingestion = Ingestion.objects.get(title=title)
        except Ingestion.DoesNotExist:
            return Response({"error": "Ingestion does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(ingestion, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['remove_product'] = request.data.get('remove_product', [])
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
