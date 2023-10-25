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
            return Response({'message': 'Veuillez fournir votre nom d’utilisateur et votre mot de passe.'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'message': 'Informations d’identification non valides.'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        response=Response({'message': 'Connexion réussie.',
                           "__SID__":request.session.session_key},status=status.HTTP_200_OK)
        return response




# endpoint qui permet à l'utilisateur de se déconnecter
class LogoutView(APIView):
    def get(self,request):
        logout(request)
        response=Response({'detail': 'Successfully logged out.'})
        response.delete_cookie('csrftoken')
        return response

# endpoint qui récupére le nom et id d'utilisateur
class WhoamiView(APIView):
    def get(self,request):
        return Response({'id': request.user.id,'username': request.user.username})

class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Interface_de_Connexion.objects.filter(visible=True)
    serializer_class = ICSerializer
