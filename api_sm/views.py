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


class MarcheFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f':
            serializer = AddMarcheSerializer()
            fields = serializer.get_fields()
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    })


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })

            return Response({'fields': field_info}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class SiteFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f':
            serializer = SiteSerializer()
            fields = serializer.get_fields()
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    })


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })

            return Response({'fields': field_info}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


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


class ClientFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l' or flag =='f':
            serializer = ClientsSerializer()
            fields = serializer.get_fields()
            if(flag=='f'): # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'name':field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    })
            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })

            return Response({'fields':field_info},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

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

    queryset = Marche.objects.all()
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











