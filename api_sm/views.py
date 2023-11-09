from django.contrib.auth import authenticate
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
    queryset = Images.objects.filter(est_bloquer=False)
    serializer_class = ICSerializer



class AddClientView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,AddClientPermission]
    def post(self,request):

        code_client=request.data.get('code_client')
        type_client=request.data.get('type_client')
        est_client_cosider=str_to_bool(request.data.get('est_client_cosider'))
        libelle_client=request.data.get('libelle_client')
        nif=request.data.get('nif')
        raison_social=request.data.get('raison_social')
        num_registre_commerce=request.data.get('num_registre_commerce')
        try:
            Clients.objects.create(code_client=code_client, type_client=type_client
                    , est_client_cosider=est_client_cosider, libelle_client=libelle_client
                    , nif=nif, raison_social=raison_social, num_registre_commerce=num_registre_commerce
                   ).save()

            return Response({'message': 'Client ajouté'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetClientsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ViewClientPermission]
    queryset = Clients.objects.filter()
    serializer_class = ClientsSerializer1


class  AddSiteView(APIView):
    permission_classes = [IsAuthenticated, AddSitePermission]
    def post(self,request):
        code_site= request.data.get('code_site')
        code_filiale= request.data.get('code_filiale')
        code_region= request.data.get('code_region')
        libelle_site= request.data.get('libelle_site')
        code_agence= request.data.get('code_agence')
        type_site=request.data.get('type_site')
        code_division= request.data.get('code_division')
        code_commune_site= request.data.get('code_commune_site')
        jour_cloture_mouv_rh_paie= request.data.get('jour_cloture_mouv_rh_paie')
        date_ouverture_site=request.data.get('date_ouverture_site')
        date_cloture_site=request.data.get('date_cloture_site')

        try:
            Sites.objects.create(code_site=code_site, code_agence=code_agence, type_site=type_site, code_filiale=code_filiale,
                  code_region=code_region, libelle_site=libelle_site, code_division=code_division,
                  code_commune_site=code_commune_site, jour_cloture_mouv_rh_paie=jour_cloture_mouv_rh_paie,
                  date_cloture_site=date_cloture_site,
                  date_ouverture_site=date_ouverture_site)
            return Response({'message': 'Site ajouté'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': "".join(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class GetSitesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ViewSitePermission]
    queryset = Sites.objects.filter()
    serializer_class = SiteSerializer1













