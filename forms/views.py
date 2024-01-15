from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_sm.Filters import *
from api_sm.Serializers import *


# Create your views here.


class UserFieldsApiView(APIView):
    def get(self, request):

        serializer = UserSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            obj = {
                    'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                }
            field_info.append(obj)
            if (field_name == "password"):
                field_info.append({
                    'name': 'confirme' + field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': 'Confirmer le mot de passe',
                })
        return Response({'fields': field_info},
                        status=status.HTTP_200_OK)

class UserFieldsStateApiView(APIView):
    def get(self, request):
        serializer = UserSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            field_info.append({
                field_name:default_value ,

            })
            state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)




class DQEFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(DQEFilter.base_filters.keys())
        serializer = DQESerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:

                obj = {
                       'name': field_name,
                       'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                }
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                     anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                     obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)


class DQEFieldsStateApiView(APIView):
    def get(self, request):
        serializer = DQESerializer()
        fields = serializer.get_fields()
        field_info = []
        dqe_pk = request.query_params.get(DQE._meta.pk.name, None)
        if dqe_pk:
            dqe = DQE.objects.get(pk=dqe_pk)
        else:
            dqe = None
        if(dqe == None):

            for field_name, field_instance in fields.items():
                if (not field_name in ['prix_q']):
                    default_value = ''
                    if str(field_instance.__class__.__name__) == 'BooleanField':
                        default_value= False
                    if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                                  'IntegerField',]:
                        default_value = 0

                    field_info.append({
                        field_name:default_value ,

                    })
                    state = {}

                    for d in field_info:
                        state.update(d)
        else:
            update_dqe=DQESerializer(dqe).data
            for field_name, field_instance in fields.items():
                if(not field_name in ['prix_q'] ):
                    if(field_name in ['prix_u','quantite']):
                        default_value = unhumanize(update_dqe[field_name])
                    else:
                        default_value = update_dqe[field_name]
                    field_info.append({
                        field_name:default_value ,

                    })
                    state = {}

                    for d in field_info:
                        state.update(d)

        return Response({'state': state}, status=status.HTTP_200_OK)

class DQEFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l' or flag =='f':
            serializer = DQESerializer()
            model_class = serializer.Meta.model
            model_name = model_class.__name__
            fields = serializer.get_fields()

            if(flag=='f'): # react form
                field_info = []

                for field_name, field_instance in fields.items():
                    print(field_name)
                    if (not field_name in ['prix_q']):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            'label': field_instance.label or field_name,

                        }
                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)

            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField") and field_name not in ['marche']:
                        obj['related'] = str(field_instance.queryset.model.__name__)
                        obj['cellRenderer']= 'InfoRenderer'
                    field_info.append(obj)


            return Response({'fields':field_info,'models':model_name,'pk':DQE._meta.pk.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class MarcheFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(MarcheFilter.base_filters.keys())
        serializer = MarcheSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                }
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)


class MarcheFieldsStateApiView(APIView):
    def get(self, request):
        serializer = MarcheSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in ['id', ]):
                if str(field_instance.__class__.__name__) == 'PrimaryKeyRelatedField':
                    default_value= ''
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value= True

                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                              'IntegerField',]:
                    default_value = 0

                field_info.append({
                    field_name:default_value ,

                })


                state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)

class MarcheFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l' or flag =='f':
            serializer = MarcheSerializer()
            fields = serializer.get_fields()
            model_class = serializer.Meta.model
            model_name = model_class.__name__

            if(flag=='f'): # react form

                field_info = []
                for field_name, field_instance in fields.items():
                    if(field_name not in ['id',]):
                        obj={
                            'name':field_name,
                            'type': str(field_instance.__class__.__name__),
                            'label': field_instance.label or field_name,
                            'source':field_instance.source
                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset']=anySerilizer(field_instance.queryset, many=True).data


                        field_info.append(obj)

            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():

                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })

            return Response({'fields':field_info,'models':model_name,'pk':Marche._meta.pk.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(ClientsFilter.base_filters.keys())
        serializer = ClientsSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                field_info.append({
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                })

        return Response({'fields': field_info},status=status.HTTP_200_OK)


class ClientFieldsStateApiView(APIView):
    def get(self, request):
        serializer = ClientsSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ""
            if str(field_instance.__class__.__name__) == 'BooleanField':
                default_value= False
            if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                          'IntegerField',]:
                default_value = 0

            field_info.append({
                field_name:default_value ,

            })
            state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)

class ClientFieldsApiView(APIView):
        def get(self, request):
            flag = request.query_params.get('flag', None)
            if flag == 'l' or flag == 'f':
                serializer = ClientsSerializer()
                fields = serializer.get_fields()
                model_class = serializer.Meta.model
                model_name = model_class.__name__
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

                return Response({'fields': field_info,'models':model_name,'pk':Clients._meta.pk.name}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_400_BAD_REQUEST)



class SiteFieldsStateApiView(APIView):
    def get(self, request):
        serializer = ClientsSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ""
            if str(field_instance.__class__.__name__) == 'BooleanField':
                default_value= False
            if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                          'IntegerField',]:
                default_value = 0

            field_info.append({
                field_name:default_value ,

            })
            state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)



class SiteFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(SitesFilter.base_filters.keys())
        serializer = SiteSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                field_info.append({
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                })

        return Response({'fields': field_info},status=status.HTTP_200_OK)
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


class NTFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(NTFilter.base_filters.keys())
        serializer = NTSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                }
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)

class NTFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f':
            serializer = NTSerializer()
            fields = serializer.get_fields()
            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    obj = {
                        'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                        obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                    field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })

            return Response({'fields': field_info,
            'models': model_name, 'pk': NT._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)




class FactureFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f' or flag == 'p': #l : liste , p : print , f : form
            serializer = FactureSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    if( not field_name in ['paye','montant_mois','montant_precedent','montant_cumule','date','heure',"marche",
                                           'projet','code_contrat','client','pole','num_travail','lib_nt',
                                           'somme','montant_rg','montant_taxe','montant_rb','a_payer','signature',
                                           'montant_marche','num_situation','tva','rabais',
                                           'retenue_garantie'] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            'label': field_instance.label or field_name,
                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    field_info.append({
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    })



            return Response({'fields': field_info,
            'models': model_name, 'pk': Factures._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class FactureFieldsStateApiView(APIView):
    def get(self, request):
        serializer = FactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in  ['paye','montant_mois','montant_precedent','montant_cumule','date','heure',"marche"]):
                if str(field_instance.__class__.__name__) == 'PrimaryKeyRelatedField':
                    default_value= ''
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value= True

                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                              'IntegerField',]:
                    default_value = 0

                field_info.append({
                    field_name:default_value ,

                })


                state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)


class FactureFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(FactureFilter.base_filters.keys())
        serializer = FactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:

                obj = {
                    'name': field_name,
                    'type': str(field_instance.__class__.__name__),
                    'label': field_instance.label or field_name,
                }
                if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                    anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                    obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data
                field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)






class EncaissementFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f' or flag == 'p': #l : liste , p : print , f : form
            serializer = EncaissementSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    if( not field_name in ['montant_creance','facture',] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            'label': field_instance.label or field_name,
                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        obj['related'] = str(field_instance.queryset.model.__name__)
                        if(field_name=="mode_paiement"):
                            obj['cellRenderer'] = 'InfoRenderer'
                    field_info.append(obj)


            return Response({'fields': field_info,
            'models': model_name, 'pk': Encaissement._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class EncaissementFieldsStateApiView(APIView):
    def get(self, request):
        serializer = EncaissementSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in  ['montant_creance','facture']):
                if str(field_instance.__class__.__name__) == 'PrimaryKeyRelatedField':
                    default_value= ''
                if str(field_instance.__class__.__name__) == 'BooleanField':
                    default_value= True

                if str(field_instance.__class__.__name__) in ['PositiveSmallIntegerField','DecimalField','PositiveIntegerField',
                                                              'IntegerField',]:
                    default_value = 0

                field_info.append({
                    field_name:default_value ,

                })


                state = {}

            for d in field_info:
                state.update(d)
        return Response({'state': state}, status=status.HTTP_200_OK)


class EncaissementFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(EncaissementFilter.base_filters.keys())
        serializer = EncaissementSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                if( field_name not in ['facture']):

                    obj = {
                        'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                        obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data
                    field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)



class DetailFactureFieldsApiView(APIView):
    def get(self, request):
        serializer = DetailFactureSerializer()
        fields = serializer.get_fields()

        model_class = serializer.Meta.model
        model_name = model_class.__name__

        field_info = []
        for field_name, field_instance in fields.items():
            if (field_name not in ['facture','detail']):
                obj = {
                    'field': field_name,
                    'headerName': field_instance.label or field_name,
                    'info': str(field_instance.__class__.__name__),
                }
                field_info.append(obj)

        return Response({'fields': field_info,
        'models': model_name, 'pk': DetailFacture._meta.pk.name}, status=status.HTTP_200_OK)


class DetailFactureFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(DetailFactureFilter.base_filters.keys())
        print(filter_fields)
        serializer = DetailFactureSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                if (field_name not in ['facture','detail']):

                    obj = {
                        'name': field_name,
                        'type': str(field_instance.__class__.__name__),
                        'label': field_instance.label or field_name,
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                        obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data
                    field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)

