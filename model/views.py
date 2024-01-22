from django.apps import apps
from django.contrib.auth import authenticate
from django.shortcuts import render

from .models import User, Diet, Product
from .serializers import UserSerializer, DietSerializer, ProductSerializer

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

#Функция получаения models определённого приложения
def get_app_models(app_label):
    app_models = apps.get_app_config(app_label).get_models()
    return app_models

#Базовая страница со списком models приложения model
def all_models(request):
    app_label = 'model'
    
    #Игнорируемые модели
    ignore_app_label = ['Gender', 'Category', 'Vitamins', 'App'] #Список model, которые игнорируются добавлением
    model_names = [model.__name__.lower()+'s' for model in get_app_models(app_label) if model.__name__ not in ignore_app_label]
    
    #Дополнительные urls
    additional_label = ['Auth-signup', 'Auth-login']
    for label in additional_label:
        model_names.append(label.lower())
        
    return render(request, 'all_models.html', {'model_names': model_names})

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
            # Пользователь аутентифицирован

            # Создаем или получаем токен для пользователя
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            # Пользователь не аутентифицирован
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            user = User.objects.get(id=firstID)
            serializer = self.get_serializer(user)
            return Response({f"User[{firstID}]": serializer.data})
        elif firstID is not None and lastID is not None:
            users = User.objects.filter(id__range=(firstID, lastID))
            serializer = self.get_serializer(users, many=True)
            return Response({f"Users[{firstID}-{lastID}]": serializer.data})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def put(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            user = User.objects.get(id=firstID)
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f"User[{firstID}] updated": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if firstID is not None and lastID is not None:
            users = User.objects.filter(id__range=(firstID, lastID))
            updated_users_data = request.data

            for user, new_data in zip(users, updated_users_data):
                serializer = self.get_serializer(user, data=new_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

            return Response({"Users updated": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def delete(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            try:
                user = User.objects.get(id=firstID)
                user.delete()
                return Response({f"User[{firstID}] deleted": "success"})
            except User.DoesNotExist:
                return Response({f"User[{firstID}]": "not found"}, status=status.HTTP_404_NOT_FOUND)
        elif firstID is not None and lastID is not None:
            users = User.objects.filter(id__range=(firstID, lastID))
            for user in users:
                user.delete()
            return Response({"Users deleted": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID or firstID and lastID"})

class DietsView(ListCreateAPIView):
    serializer_class =  DietSerializer
    
    def get(self, request):
        diets = Diet.objects.all()
        serializer = self.get_serializer(diets, many=True)
        return Response({"Diets": serializer.data})
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Diet created": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DietView(RetrieveUpdateDestroyAPIView):
    serializer_class = DietSerializer

    def get(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            diet = Diet.objects.get(id=firstID)
            serializer = self.get_serializer(diet)
            return Response({f"User[{firstID}]": serializer.data})
        elif firstID is not None and lastID is not None:
            diets = Diet.objects.filter(id__range=(firstID, lastID))
            serializer = self.get_serializer(diets, many=True)
            return Response({f"Diets[{firstID}-{lastID}]": serializer.data})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def put(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            diet = Diet.objects.get(id=firstID)
            serializer = self.get_serializer(diet, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f"Diet[{firstID}] updated": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if firstID is not None and lastID is not None:
            diets = Diet.objects.filter(id__range=(firstID, lastID))
            updated_users_data = request.data

            for user, new_data in zip(diets, updated_users_data):
                serializer = self.get_serializer(user, data=new_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

            return Response({"Diets updated": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def delete(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            try:
                diet = Diet.objects.get(id=firstID)
                diet.delete()
                return Response({f"User[{firstID}] deleted": "success"})
            except User.DoesNotExist:
                return Response({f"User[{firstID}]": "not found"}, status=status.HTTP_404_NOT_FOUND)
        elif firstID is not None and lastID is not None:
            diets = Diet.objects.filter(id__range=(firstID, lastID))
            for diet in diets:
                diet.delete()
            return Response({"Diets deleted": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID or firstID and lastID"})
            
class ProductsView(ListCreateAPIView):
    serializer_class =  ProductSerializer
    
    def get(self, request):
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response({"Products": serializer.data})
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Product created": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            product = Product.objects.get(id=firstID)
            serializer = self.get_serializer(product)
            return Response({f"User[{firstID}]": serializer.data})
        elif firstID is not None and lastID is not None:
            products = Product.objects.filter(id__range=(firstID, lastID))
            serializer = self.get_serializer(products, many=True)
            return Response({f"Products[{firstID}-{lastID}]": serializer.data})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def put(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            product = Product.objects.get(id=firstID)
            serializer = self.get_serializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f"Product[{firstID}] updated": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if firstID is not None and lastID is not None:
            products = Product.objects.filter(id__range=(firstID, lastID))
            updated_users_data = request.data

            for user, new_data in zip(products, updated_users_data):
                serializer = self.get_serializer(user, data=new_data, partial=True)
                if serializer.is_valid():
                    serializer.save()

            return Response({"Products updated": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID and lastID"})
        
    def delete(self, request, firstID=None, lastID=None):
        if firstID is not None and lastID is None:
            try:
                product = Product.objects.get(id=firstID)
                product.delete()
                return Response({f"User[{firstID}] deleted": "success"})
            except User.DoesNotExist:
                return Response({f"User[{firstID}]": "not found"}, status=status.HTTP_404_NOT_FOUND)
        elif firstID is not None and lastID is not None:
            products = Product.objects.filter(id__range=(firstID, lastID))
            for product in products:
                product.delete()
            return Response({"Products deleted": f"from {firstID} to {lastID}"})
        else:
            return Response({"error": "Provide valid parameters for firstID or firstID and lastID"})      

        
