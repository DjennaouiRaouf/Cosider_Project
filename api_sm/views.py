import json

from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from import_export.admin import ImportMixin, ExportMixin
from import_export.results import RowResult
from rest_framework import generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from tablib import Dataset
from .Filters import *
from .Resources import DQEResource
from .Serializers import *
from .models import *
from .tools import *
import  numpy as np

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = []
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        app_name = 'api_sm'

        if user is not None:
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            app_permissions = self.get_app_permissions(user, app_name)
            response = Response(status=status.HTTP_200_OK)
            role = '|'.join(list(app_permissions))
            response.set_cookie('token', token.key)
            response.set_cookie('role', role)
            return response
        else:
            return Response({'message': 'Informations d’identification non valides'}, status=status.HTTP_400_BAD_REQUEST)

    def get_app_permissions(self, user, app_name):
        # Get all permissions for the specified app
        all_permissions = user.get_all_permissions()
        app_permissions = set()

        for permission in all_permissions:
            if permission.split('.')[0] == app_name:
                app_permissions.add(permission)

        return app_permissions



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Token.objects.get(user_id=request.user.id).delete()
        response=Response({'message': 'Vous etes déconnecté'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')
        response.delete_cookie('role')
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
    permission_classes = [permissions.IsAuthenticated, ViewClientPermission]
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientsFilter


class AjoutSiteApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,AddSitePermission]

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
    permission_classes = [IsAuthenticated, AddMarchePermission]

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
    permission_classes = [IsAuthenticated, AddDQEPermission]
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
    permission_classes = [permissions.IsAuthenticated, ViewSitePermission]

    queryset = Sites.objects.all()
    serializer_class = SiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SitesFilter




class GetMarcheView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ViewMarchePermission]
    queryset = Marche.objects.all()
    serializer_class = MarcheSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MarcheFilter


class GetDQEView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,ViewDQEPermission]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DQEFilter


class ImportDQEAPIView(ImportMixin,  APIView):
    permission_classes = [IsAuthenticated, UploadDQEPermission]
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        resource = DQEResource()
        dataset = Dataset()
        dqe = request.FILES['file']
        marche=request.data.get(Marche._meta.pk.name)
        imported_data = dataset.load(dqe.read())
        filtered_rows = [row for row in imported_data.dict if row['marche'] == marche]
        filtered_dataset = Dataset()
        filtered_dataset.headers = imported_data.headers
        filtered_dataset.extend([row.values() for row in filtered_rows])
        result = resource.import_data(filtered_dataset, dry_run=True)

        try:
            resource.import_data(filtered_dataset, dry_run=False)
            return Response({'message': 'Import successful'}, status=200)
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class GetNTView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,ViewNTPermission]
    queryset = NT.objects.all()
    serializer_class = NTSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NTFilter


class AjoutNTApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, AddNTPermission]
    queryset = NT.objects.all()
    serializer_class = NTSerializer

    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            custom_response = {
                'status': 'success',
                'message': 'NT ajouté',
                'data': serializer.data,
            }

            return Response(custom_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            custom_response = {
                'status': 'error',
                'message': str(e),
                'data': None,
            }

            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

class GetDQEbyId(generics.ListAPIView):
    queryset = DQE.objects.all()
    serializer_class = DQESerializer
    lookup_field = 'marche'

class GetFacture(generics.ListAPIView):
    queryset = Factures.objects.all()
    serializer_class = FactureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FactureFilter


class GetEncaissement(generics.ListAPIView):
    queryset = Encaissement.objects.all().order_by('-date_encaissement')
    serializer_class = EncaissementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EncaissementFilter


class GetFactureRG(generics.ListAPIView):
    queryset = Factures.objects.all()
    serializer_class = FactureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FactureFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total = queryset.aggregate(montant_rg=models.Sum('montant_rg'))['montant_rg']
        response_data = super().list(request, *args, **kwargs).data
        return Response({'factures':response_data,
                         'extra':{
                             'total_rg': total,
                             'total_rgl':num2words(total, to='currency', lang='fr_DZ').upper(),
                              'code_contrat':queryset[0].marche.code_contrat,
                             'signature': queryset[0].marche.date_signature,
                             'projet': queryset[0].marche.libelle,
                             'montant_marche':queryset[0].marche.ht,
                             'client': queryset[0].marche.nt.code_client.id,
                             'nt': queryset[0].marche.nt.nt,
                             'lib_nt': queryset[0].marche.nt.libelle,
                            'pole':queryset[0].marche.nt.code_site.id,

                         }},status=status.HTTP_200_OK)


class DelDQEByID(generics.DestroyAPIView,DestroyModelMixin):
    permission_classes = [IsAuthenticated,DeleteDQEPermission]
    queryset = DQE.objects.all()
    serializer_class = DQESerializer

    def delete(self, request, *args, **kwargs):
        pk_list = request.data.get(DQE._meta.pk.name)
        if pk_list:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(pk__in=pk_list)
            self.perform_destroy(queryset)

        return Response({'Message': pk_list},status=status.HTTP_200_OK)


class UpdateDQEApiVew(generics.UpdateAPIView):
    queryset = DQE.objects.all()
    serializer_class = DQESerializer




class AddFactureApiView(generics.CreateAPIView):
    queryset = Factures.objects.all()
    serializer_class = FactureSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': 'Facture ajoutée',
            'data': serializer.data,
        }

        return Response(custom_response, status=status.HTTP_201_CREATED)


class AddEncaissement(generics.CreateAPIView):
    queryset = Encaissement.objects.all()
    serializer_class = EncaissementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        custom_response = {
            'status': 'success',
            'message': "L'Encaissement c'est deroulé avec succé",
            'data': serializer.data,
        }

        return Response(custom_response, status=status.HTTP_201_CREATED)


class OptionImpressionApiView(generics.ListAPIView):
    serializer_class = OptionImpressionSerializer
    def get_queryset(self):
        option = self.request.query_params.get('option', None)

        if option in ["1","0"]:
            if(option == "1"):
                return OptionImpression.objects.filter(type__in=['H', 'F'])

            if(option == "0"):
                return OptionImpression.objects.filter(type__in=['EH', 'EF'])

        else:
            Response(status=status.HTTP_400_BAD_REQUEST)




class DeletedDQE(generics.ListAPIView):
    queryset = DQE.all_objects.deleted_only()
    serializer_class = DQESerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DQEFilter


class LibUM(generics.ListAPIView):
    queryset = TabUniteDeMesure.objects.all()
    serializer_class = UniteDeMesureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UMFilter


class LibMP(generics.ListAPIView):
    queryset = ModePaiement.objects.all()
    serializer_class = ModePaiementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MPFilter



class getDetailFacture(generics.ListAPIView):
    queryset = DetailFacture.objects.all()
    serializer_class = DetailFactureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DetailFactureFilter


class GetAvance(generics.ListAPIView):
    permission_classes = [IsAuthenticated,ViewAvancePermission]
    queryset = Avance.objects.all()
    serializer_class = AvanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvanceFilter



class LibAV(generics.ListAPIView):
    queryset = TypeAvance.objects.all()
    serializer_class = TypeAvanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TypeAvanceFilter

class LibCaut(generics.ListAPIView):
    queryset = TypeCaution.objects.all()
    serializer_class = TypeCautionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TypeCautionFilter


class AddAvanceApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,AddAvancePermission]
    queryset = Avance.objects.all()
    serializer_class = AvanceSerializer


    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            custom_response = {
                'status': 'success',
                'message': 'Avance ajouté',
                'data': serializer.data,
            }

            return Response(custom_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            custom_response = {
                'status': 'error',
                'message': str(e),
                'data': None,
            }

            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)



class GetCautions(generics.ListAPIView):
    queryset = Cautions.objects.all()
    serializer_class = CautionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CautionFilter


class PermissionApiView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        user_permissions = self.request.user.get_all_permissions()
        return Response({"permissions": user_permissions})
        '''
        app_name = 'api_sm'
        app_permissions = self.get_app_permissions(request.user, app_name)
        role = '|'.join(list(app_permissions))
        return Response({"role":role},status=status.HTTP_200_OK)

    def get_app_permissions(self, user, app_name):
        # Get all permissions for the specified app
        all_permissions = user.get_all_permissions()
        app_permissions = set()

        for permission in all_permissions:
            if permission.split('.')[0] == app_name:
                app_permissions.add(permission)

        return app_permissions


class AddCautions(generics.CreateAPIView):
    queryset = Cautions.objects.all()
    serializer_class = CautionSerializer


    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            custom_response = {
                'status': 'success',
                'message': 'Caution ajouté',
                'data': serializer.data,
            }

            return Response(custom_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            custom_response = {
                'status': 'error',
                'message': str(e),
                'data': None,
            }

            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)


class GetODS(generics.ListAPIView):
    permission_classes = [IsAuthenticated,ViewODSPermission]
    queryset = Ordre_De_Service.objects.all()
    serializer_class = Ordre_De_ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Ordre_De_ServiceFilter



class AddODS(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,AddODSPermission]
    queryset = Ordre_De_Service.objects.all()
    serializer_class = Ordre_De_ServiceSerializer


    def create(self, request, *args, **kwargs):
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            custom_response = {
                'status': 'success',
                'message': 'ODS ajouté',
                'data': serializer.data,
            }

            return Response(custom_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            custom_response = {
                'status': 'error',
                'message': str(e),
                'data': None,
            }

            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)