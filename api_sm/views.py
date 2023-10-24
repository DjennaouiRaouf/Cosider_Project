from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .Serializers import *
from .models import *



# endpoint qui permet à l'utilisateur de se connecter
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
        session_id = request.session.session_key
        response=Response({'message': 'Successfully logged in.'},status=status.HTTP_200_OK)
        response.set_cookie("__SID__",session_id)

        return response




# endpoint qui permet à l'utilisateur de se déconnecter
class LogoutView(APIView):

    def get(self,request):
        logout(request)
        response=Response({'detail': 'Successfully logged out.'})
        response.delete_cookie('csrftoken')
        response.delete_cookie('__SID__')
        return response


# endpoint qui récupére le nom et id d'utilisateur
class WhoamiView(APIView):
    def get(self,request):
        return Response({'id': request.user.id,'username': request.user.username})



class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Interface_de_Connexion.objects.filter(visible=True)
    serializer_class = ICSerializer
