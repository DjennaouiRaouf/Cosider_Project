from rest_framework import serializers
from api_sm.models import *



class ICSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'


class ClientsSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ['code_client','type_client','est_client_cosider','libelle_client','nif',
                  'raison_social','num_registre_commerce']


class SiteSerializer1(serializers.ModelSerializer):
    class Meta:
        modem = Sites
        fields =  '__all__'