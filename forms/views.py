from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_sch.Serializers import ProductionSerializer
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
                        "required": field_instance.required,
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
                        default_value = update_dqe[field_name]
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

                    if (not field_name in ['prix_q','id']):
                        if( field_name in ['prix_u','quantite']):
                            readOnly=False
                        else:
                            readOnly = True
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                            'readOnly': readOnly
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
                    if(field_name in ['prix_u','prix_q','quantite']):
                        obj['cellRenderer']='InfoRenderer'
                    if (field_name in ['unite']):
                        obj['hide']=True
                    field_info.append(obj)


            return Response({'fields':field_info,'models':model_name,'pk':DQE._meta.pk.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class MarcheFieldsFilterApiView(APIView):
    def get(self,request):
        field_info = []

        for field_name, field_instance  in MarcheFilter.base_filters.items():


            obj = {
                'name': field_name,
                'type': str(field_instance.__class__.__name__),
                'label': field_instance.label or field_name,

            }
            if str(field_instance.__class__.__name__) == 'ModelChoiceFilter':
                anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data


            field_info.append(obj)

        return Response({'fields': field_info},status=status.HTTP_200_OK)


class MarcheFieldsStateApiView(APIView):
    def get(self, request):
        serializer = MarcheSerializer()
        fields = serializer.get_fields()
        field_info = []
        marche_pk = request.query_params.get(Marche._meta.pk.name, None)
        if marche_pk:
            marche = Marche.objects.get(pk=marche_pk)
        else:
            marche = None
        if(marche == None):

            for field_name, field_instance in fields.items():
                if (field_name not in ['id', 'ht', 'ttc']):
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
            update_marche=MarcheSerializer(marche).data
            for field_name, field_instance in fields.items():

                    default_value = update_marche[field_name]
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
                    if(field_name not in ['ht','ttc']):

                        if (field_name in ['id','nt','code_site',"libelle"]):
                            readOnly = True
                        else:
                            readOnly = False

                        obj={
                            'name':field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                            'source':field_instance.source,
                            'readOnly': readOnly
                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset']=anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)

            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():

                    obj={
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),
                    }

                    if (field_name in ['rg','rabais', 'ttc', 'ht']):
                        obj['cellRenderer'] = 'InfoRenderer'

                    field_info.append(obj)
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
                            "required": field_instance.required,
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
                        "required": field_instance.required,
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
                        "required": field_instance.required,
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
        if flag == 'l' or flag == 'f' or flag == 'p': 
            serializer = FactureSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():
                    if( field_name in ['numero_facture','du','au'] ):

                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                            
                        }


                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    obj={
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),

                    }
                    if(field_name in ['client','signature','montant_marche','pole','lib_nt','projet','somme','marche','heure',
                                      'num_travail',]):
                        obj['hide']= True
                    if (field_name in ['montant_cumule','montant_mois','montant_precedent','montant_rg','montant_taxe','montant_rb',"montant_factureHT",'montant_factureTTC']):
                        obj['cellRenderer'] = 'InfoRenderer'
                    field_info.append(obj)



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
                if field_name not in ['marche']:
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
        if flag == 'l' or flag == 'f' or flag == 'p': 
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
                            "required": field_instance.required,
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
                        'cellRenderer': 'InfoRenderer'
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        obj['related'] = str(field_instance.queryset.model.__name__)

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








class AvanceFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f' : 
            serializer = AvanceSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []

                for field_name, field_instance in fields.items():

                    if( not field_name in ['montant','heure','marche','id','num_avance','remboursee'] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                            

                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    if (field_name not in ["id"]):
                        field_info.append({
                            'field': field_name,
                            'headerName': field_instance.label or field_name,
                            'info': str(field_instance.__class__.__name__),
                        })



            return Response({'fields': field_info,
            'models': model_name, 'pk': Avance._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class AvanceFieldsStateApiView(APIView):
    def get(self, request):
        serializer = AvanceSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in  ['montant','heure','marche','id']):
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


class CautionFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        marche = request.query_params.get('marche', None)

        if flag == 'l' or flag == 'f' :
            serializer = CautionSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__
            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():

                    if( not field_name in ['est_recupere','marche','montant','id'] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                            

                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            if(str(field_instance.queryset.model.__name__)=="Avance"):
                                obj['queryset'] = AvanceSerializer(field_instance.queryset.filter(marche=marche), many=True).data


                            else:
                                anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                                obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)


            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                for field_name, field_instance in fields.items():
                    if (field_name not in ['heure','marche']):
                        obj={
                            'field': field_name,
                            'headerName': field_instance.label or field_name,
                            'info': str(field_instance.__class__.__name__),

                        }
                        if(str(field_instance.__class__.__name__) != 'BooleanField' ):
                            obj['cellRenderer']='InfoRenderer'

                        field_info.append(obj)



            return Response({'fields': field_info,
            'models': model_name, 'pk': Cautions._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)





class CautionFieldsStateApiView(APIView):
    def get(self, request):
        serializer = CautionSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in  ['est_recupere','marche','montant']):
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






class ODSFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f' or flag == 'p':
            serializer = Ordre_De_ServiceSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__

            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():

                    if( not field_name in ['marche',] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                        }
                        if(str(field_instance.style.get("base_template")).find('textarea')!=-1):
                            obj['textarea']=True
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
                        'cellRenderer' : 'InfoRenderer'
                    }
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        obj['related'] = str(field_instance.queryset.model.__name__)


                    field_info.append(obj)


            return Response({'fields': field_info,
            'models': model_name, 'pk': Ordre_De_Service._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)




class OdsFieldsFilterApiView(APIView):
    def get(self,request):
        filter_fields = list(Ordre_De_ServiceFilter.base_filters.keys())

        serializer = Ordre_De_ServiceSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            if field_name in filter_fields:
                if (field_name not in ['marche']):

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


class OdsFieldsStateApiView(APIView):
    def get(self, request):
        serializer = Ordre_De_ServiceSerializer()
        fields = serializer.get_fields()
        field_info = []


        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in  ['marche']):
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



class FlashFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l':
            serializer = ProductionSerializer()
            fields = serializer.get_fields()
            model_class = serializer.Meta.model
            model_name = model_class.__name__


            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                obj1 = {
                    "headerName": 'Contractuel',
                    "children": []
                }
                obj2 = {
                    "headerName": 'Supplementaire',
                    "children": []
                }
                obj3 = {
                    "headerName": 'Complementaire',
                    "children": []
                }

                for field_name, field_instance in fields.items():
                    if(field_name not in ['prevu_realiser','est_cloturer','user_id','date_modification']):

                        obj={
                                'field': field_name,
                                'headerName': field_instance.label or field_name,
                                'info': str(field_instance.__class__.__name__),
                        }
                        if (str(field_name).startswith('valeur') or str(field_name).startswith('quantite')):
                            obj['cellRenderer'] = 'InfoRenderer'

                        if (field_name  in ['quantite_1', 'valeur_1']):
                            obj1['children'].append(obj)
                        if (field_name  in ['quantite_2', 'valeur_2']):
                            obj2['children'].append(obj)
                        if (field_name  in ['quantite_3', 'valeur_3']):
                            obj3['children'].append(obj)

                        if(field_name not in ['quantite_1', 'valeur_1','quantite_2', 'valeur_2','quantite_3', 'valeur_3']):
                            field_info.append(obj)



                field_info.append(obj1)
                field_info.append(obj2)
                field_info.append(obj3)

            return Response({'fields':field_info,'models':model_name,'pk':Marche._meta.pk.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)






class FlashFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l':
            serializer = ProductionSerializer()
            fields = serializer.get_fields()
            model_class = serializer.Meta.model
            model_name = model_class.__name__


            if(flag=='l'): #data grid list (react ag-grid)
                field_info = []
                field_info2 = []
                obj1 = {
                    "headerName": 'Contractuel',
                    "children": []
                }
                obj2 = {
                    "headerName": 'Supplementaire',
                    "children": []
                }
                obj3 = {
                    "headerName": 'Complementaire',
                    "children": []
                }

                for field_name, field_instance in fields.items():
                    if(field_name not in ['prevu_realiser','est_cloturer','user_id','date_modification']):

                        obj={
                                'field': field_name,
                                'headerName': field_instance.label or field_name,
                                'info': str(field_instance.__class__.__name__),
                        }
                        if (str(field_name).startswith('valeur') or str(field_name).startswith('quantite')):
                            obj['cellRenderer'] = 'InfoRenderer'

                        if (field_name  in ['quantite_1', 'valeur_1']):
                            obj1['children'].append(obj)
                        if (field_name  in ['quantite_2', 'valeur_2']):
                            obj2['children'].append(obj)
                        if (field_name  in ['quantite_3', 'valeur_3']):
                            obj3['children'].append(obj)

                        field_info2.append(obj)
                        if(field_name not in ['quantite_1', 'valeur_1','quantite_2', 'valeur_2','quantite_3', 'valeur_3']):
                            field_info.append(obj)



                field_info.append(obj1)
                field_info.append(obj2)
                field_info.append(obj3)

            return Response({'fields':field_info,"fields2":field_info2,'models':model_name,'pk':Marche._meta.pk.name},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class AttachementsFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f':
            serializer = AttachementsSerializer()
            fields = serializer.get_fields()

            model_class = serializer.Meta.model
            model_name = model_class.__name__

            if (flag == 'f'):  # react form
                field_info = []
                for field_name, field_instance in fields.items():

                    if(  field_name in ['qte_mois','montant_mois',"date"] ):
                        obj = {
                            'name': field_name,
                            'type': str(field_instance.__class__.__name__),
                            "required": field_instance.required,
                            'label': field_instance.label or field_name,
                        }

                        if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                            anySerilizer = create_dynamic_serializer(field_instance.queryset.model)
                            obj['queryset'] = anySerilizer(field_instance.queryset, many=True).data

                        field_info.append(obj)
                return Response({'fields': field_info,
                             'models': model_name, 'pk': Ordre_De_Service._meta.pk.name}, status=status.HTTP_200_OK)

            if (flag == 'l'):  # data grid list (react ag-grid)
                field_info = []
                field_info2 = []
                obj1 = {
                    "headerName": 'Qauntite',
                    "children": [],
                    'cellRenderer': 'InfoRenderer'

                }
                obj2 = {
                    "headerName": 'Montant',
                    "children": [],
                    'cellRenderer': 'InfoRenderer'
                }
                for field_name, field_instance in fields.items():

                    obj = {
                        'field': field_name,
                        'headerName': field_instance.label or field_name,
                        'info': str(field_instance.__class__.__name__),

                    }
                    if(field_name in ['prix_u']):
                        obj['cellRenderer'] = 'InfoRenderer'
                    if (str(field_instance.__class__.__name__) == "PrimaryKeyRelatedField"):
                        obj['related'] = str(field_instance.queryset.model.__name__)
                    field_info2.append(obj)
                    if (field_name in ['qte_precedente','qte_mois','qte_cumule']):
                        obj['cellRenderer'] = 'InfoRenderer'
                        obj1['children'].append(obj)

                    if (field_name in ['montant_precedent','montant_mois','montant_cumule']):
                        obj['cellRenderer'] = 'InfoRenderer'
                        obj2['children'].append(obj)
                    if (field_name not in ['montant_precedent', 'montant_mois', 'montant_cumule','qte_precedente','qte_mois','qte_cumule','marche']):
                        field_info.append(obj)

                field_info.append(obj1)
                field_info.append(obj2)


            return Response({'fields': field_info,"fields2":field_info2,
            'models': model_name, 'pk': Ordre_De_Service._meta.pk.name}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)






class AttFieldsStateApiView(APIView):
    def get(self, request):
        serializer = AttachementsSerializer()
        fields = serializer.get_fields()
        field_info = []


        for field_name, field_instance in fields.items():
            default_value = ''
            if(  field_name in ['qte_mois','montant_mois',"date"] ):

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
