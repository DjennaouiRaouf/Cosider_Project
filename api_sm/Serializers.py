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





class MarcheSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(source='nt_code_site_code_site',write_only=True)
    nt = serializers.CharField(source='nt_nt',write_only=True)

    class Meta:
        model = Marche
        fields = "__all__"

    def create(self, validated_data):
        code_site = validated_data.pop('nt_code_site_code_site')
        nt = validated_data.pop('nt_nt')
        nt_obj = NT.objects.get(
            nt=nt,
            code_site__code_site=code_site
        )
        marche = Marche.objects.create(nt=nt_obj, **validated_data)
        return marche



    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('num_avenant', None)
        fields.pop('id', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ht'] = instance.ttc
        representation['ttc'] = instance.ttc
        representation['code_site'] = instance.nt.code_site.code_site
        representation['nt'] = instance.nt.nt

        return representation





