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
        fiels=['code_site','code_filiale', 'code_region','libelle_site','code_agence', 'type_site',
        'code_division','code_commune_site','jour_cloture_mouv_rh_paie', 'date_ouverture_site','date_cloture_site'
        ]