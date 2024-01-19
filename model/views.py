from django.apps import apps
from django.shortcuts import render

from .models import User
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

#Функция получаения models определённого приложения
def get_app_models(app_label):
    app_models = apps.get_app_config(app_label).get_models()
    return app_models

#Базовая страница со списком models приложения model
def all_models(request):
    app_label = 'model'
    ignore_app_label = ['Gender'] #Список model, которые игнорируются добавлением
    model_names = [model.__name__.lower()+'s' for model in get_app_models(app_label) if model.__name__ not in ignore_app_label]
    
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

        
            
        
        
        
