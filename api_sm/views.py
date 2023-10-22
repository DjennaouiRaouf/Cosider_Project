from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .Serializers import *
from .models import *


# Create your views here.
class CSRFView(APIView):
    def get(self,request):
            response = Response({'message': 'CSRF cookie set'})
            response['X-CSRFToken'] = get_token(request)
            return response

class LoginView(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        if username is None or password is None:
            return Response({'message': 'Please provide username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        response=Response({'message': 'Successfully logged in.'},status=status.HTTP_200_OK)
        response.set_cookie('__isAuth__', 'true', max_age=None)
        return response

class LogoutView(APIView):
    def get(self,request):
        logout(request)
        return Response({'detail': 'Successfully logged out.','uname':request.user.username})

class WhoamiView(APIView):
    def get(self,request):
        return Response({'id': request.user.id,'username': request.user.username})

class SessionView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({'isAuthenticated': False})

        return Response({'isAuthenticated': True})
class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Interface_de_Connexion.objects.filter(visible=True)
    serializer_class = ICSerializer
