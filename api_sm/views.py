from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .Serializers import *
from .models import *
from .tools import *


class LoginView(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            response=Response({'message': 'Invalid credentials'}, status=status.HTTP_200_OK)
            response.set_cookie('token', token.key)
            return response
        else:
            return Response({'message': 'Informations d’identification non valides'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Token.objects.get(user_id=request.user.id).delete()
        response=Response({'message': 'Vous etes déconnecté'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')
        return response



class WhoamiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'whoami':request.user.username}, status=status.HTTP_200_OK)

class GetICImages(generics.ListAPIView):
    permission_classes = []
    queryset = Images.objects.filter()
    serializer_class = ICSerializer





class AjoutClientApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, AddClientPermission]
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': 'Client ajouté',
            'data': serializer.data,
        }


        return Response(custom_response, status=status.HTTP_201_CREATED)


class GetClientsView(generics.ListAPIView):

    queryset = Clients.objects.filter()
    serializer_class = ClientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code_client', 'type_client', 'est_client_cosider','est_client_cosider','libelle_client']


class AjoutSiteApiView(generics.CreateAPIView):

    queryset = Sites.objects.all()
    serializer_class = SiteSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': 'Site ajouté',
            'data': serializer.data,
        }
        return Response(custom_response, status=status.HTTP_201_CREATED)


class AjoutMarcheApiView(generics.CreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = MarcheSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': 'Marché ajouté',
            'data': serializer.data,
        }

        return Response(custom_response, status=status.HTTP_201_CREATED)


class AjoutMarcheApiView(generics.CreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = MarcheSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': 'Marché ajouté',
            'data': serializer.data,
        }

        return Response(custom_response, status=status.HTTP_201_CREATED)


class AjoutDQEApiView(generics.CreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = DQESerializer

    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            custom_response = {
                'status': 'success',
                'message': 'DQE ajouté',
                'data': serializer.data,
            }

            return Response(custom_response, status=status.HTTP_201_CREATED)
        except Exception as e :
            custom_response = {
                'status': 'error',
                'message': str(e),
                'data': None,
            }

            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

class GetSitesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ViewSitePermission]
    queryset = Sites.objects.all()
    serializer_class = SiteSerializer



class GetMarcheView(generics.ListAPIView):
    queryset = Marche.objects.all().order_by('nt', 'num_avenant')
    serializer_class = MarcheSerializer


class GetDQEView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer



class GetNTView(generics.ListAPIView):
    queryset = NT.objects.all()
    serializer_class = NTSerializer

class AjoutNTApiView(generics.CreateAPIView):
    queryset = NT.objects.all()
    serializer_class = NTSerializer


