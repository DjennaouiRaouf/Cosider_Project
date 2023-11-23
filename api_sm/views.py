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
    serializer_class = ClientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code_client', 'type_client', 'est_client_cosider','est_client_cosider','libelle_client']

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
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)

    
class GetSitesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ViewSitePermission]
    queryset = Sites.objects.filter()
    serializer_class = SiteSerializer


class GetMarcheView(generics.ListAPIView):

    queryset = Marche.objects.filter(avenant_du_contrat__isnull=True)
    serializer_class = ListMarcheSerializer


class GetDQEView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DQE.objects.all()
    serializer_class = ListMarcheSerializer

class AddDQEView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        site=request.data.get('site')
        nt=request.data.get('nt')
        avenant=request.data.get('avenant')
        designation=request.data.get('designation')
        unite=request.data.get('unite')
        prix_u=request.data.get('prix_u')
        quantite=request.data.get('quantite')

        marche = Marche.objects.get(nt__nt=nt, nt__code_site__code_site=site,
                                    num_avenant=avenant)
        if(marche):
            try:
                DQE(marche=marche,designation=designation,unite=unite,prix_u=prix_u,quantite=quantite).save()
                return Response({'message': "Vous avez ajouté un DQE"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'message': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': "Ce marché n'existe pas"},
                            status=status.HTTP_400_BAD_REQUEST)





class AddMacheView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        code_site=request.data.get('code_site')
        num_nt=request.data.get('num_nt')
        libelle=request.data.get('libelle')
        rg= request.data.get('retenue_garantie')
        ods_depart=request.data.get('ods_depart')
        date_signature= request.data.get('date_signature')
        delais=request.data.get('delais')
        revisable=str_to_bool(request.data.get('revisable'))
        rabais=request.data.get('rabais')
        tva=request.data.get('tva')
        code_contrat=request.data.get('num_contrat')
        nouveau = str_to_bool(request.data.get('nouveau'))
        if (nouveau == False):  # ajouter un avenant
            try:
                marche = Marche.objects.get(nt__nt=num_nt, nt__code_site__code_site=code_site,
                                            avenant_du_contrat__isnull=True)

                if (marche.id):
                    site = Sites.objects.get(code_site=code_site)

                    nt = NT.objects.get(code_site=site, nt=num_nt)
                    Marche(nt=nt, libelle=libelle, ods_depart=ods_depart, delais=delais, date_signature=date_signature,
                           revisable=revisable, rabais=rabais, tva=tva, code_contrat=code_contrat,retenue_de_garantie=rg,
                           avenant_du_contrat=marche).save()
                    return Response({'message': "Vous avez ajouté un avenant"}, status=status.HTTP_200_OK)

                else:
                    return Response(
                        {'message': "Ce marche ne paut pas etre un avenant (le marché initial n'existe pas )"},
                        status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'message': "Ce marche ne paut pas etre un avenant (le marché initial n'existe pas )"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                site = Sites.objects.get(code_site=code_site)
                nt = NT.objects.get(code_site=site, nt=num_nt)
                Marche(nt=nt,
                       libelle=libelle, ods_depart=ods_depart, delais=delais,
                       revisable=revisable, rabais=rabais, tva=tva, code_contrat=code_contrat,retenue_de_garantie=rg,
                       avenant_du_contrat=None).save()
                return Response({'message': "Vous avez créé un nouveau marché"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': "Impossible de créer un nouveau marché"},
                                status=status.HTTP_400_BAD_REQUEST)











