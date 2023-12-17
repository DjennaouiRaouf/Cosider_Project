from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class DQEFieldsStateApiView(APIView):
    def get(self, request):
        serializer = DQESerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
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
        return Response({'state': state}, status=status.HTTP_200_OK)

class DQEFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag',None)
        if flag=='l' or flag =='f':
            serializer = DQESerializer()
            fields = serializer.get_fields()
            if(flag=='f'): # react form
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


class MarcheFieldsStateApiView(APIView):
    def get(self, request):
        serializer = MarcheSerializer()
        fields = serializer.get_fields()
        field_info = []
        for field_name, field_instance in fields.items():
            default_value = ''
            if (field_name not in ['id', 'num_avenant']):
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
                    if(field_name not in ['id','num_avenant']):
                        obj={
                            'name':field_name,
                            'type': str(field_instance.__class__.__name__),
                            'label': field_instance.label or field_name,
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
                print(model_name)
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

                return Response({'fields': field_info,'models':model_name}, status=status.HTTP_200_OK)
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


class NTFieldsApiView(APIView):
    def get(self, request):
        flag = request.query_params.get('flag', None)
        if flag == 'l' or flag == 'f':
            serializer = NTSerializer()
            fields = serializer.get_fields()
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

            return Response({'fields': field_info}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)



