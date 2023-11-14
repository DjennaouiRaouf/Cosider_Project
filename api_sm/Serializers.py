from rest_framework import serializers
from api_sm.models import *



class ICSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sites
        fields = '__all__'



class NTSerializer(serializers.ModelSerializer):
    code_site=SiteSerializer()
    code_client=ClientsSerializer()
    class Meta:
        model=NT
        fields ='__all__'

class MarcheSerializer(serializers.ModelSerializer):
    nt=NTSerializer()
    class Meta:
        model=Marche
        fields= '__all__'
