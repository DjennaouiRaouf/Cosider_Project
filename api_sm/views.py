from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .Serializers import *
from .models import *

class LoginView(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response=Response({'message': 'Invalid credentials'}, status=status.HTTP_200_OK)
            response.set_cookie('token', token.key)
            return response
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



class WhoamiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'whoami':request.user.username}, status=status.HTTP_200_OK)

class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Images.objects.filter(visible=True)
    serializer_class = ICSerializer



class AddClientView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        code_client=request.data.get('code_client')
        type_client=request.data.get('type_client')
        est_client_cosider=True
        libelle_client=request.data.get('libelle_client')
        nif=request.data.get('nif')
        raison_social=request.data.get('raison_social')
        num_registre_commerce=request.data.get('num_registre_commerce')
        Clients(code_client=code_client,type_client=type_client
                ,est_client_cosider=est_client_cosider,libelle_client=libelle_client
                ,nif=nif,raison_social=raison_social,num_registre_commerce=num_registre_commerce).save()
        return Response({'message':'123' }, status=status.HTTP_200_OK)











