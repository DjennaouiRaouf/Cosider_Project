from rest_framework import serializers
from api_sm.models import *



class ICSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'

class ClientsSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields



    class Meta:
        model = Clients
        fields = '__all__'








class SiteSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    class Meta:
        model = Sites
        fields = '__all__'











class NTSerializer(serializers.ModelSerializer):
    code_site=SiteSerializer()
    code_client=ClientsSerializer()


    class Meta:
        model=NT
        fields ='__all__'


class ListMarcheSerializer(serializers.ModelSerializer):

    class Meta:
        model=Marche
        fields= "__all__"




class DQESerializer(serializers.ModelSerializer):
    class Meta:
        model=DQE
        fields='__al__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prix_q'] = instance.prix_q
        return representation



class ListMarcheSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ht'] = instance.ttc
        representation['ttc'] = instance.ttc
        representation['code_site'] = instance.nt.code_site.code_site
        representation['nt'] = instance.nt.nt

        return representation
    class Meta:
        model=Marche
        fields="__all__"





