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
    code_site = serializers.CharField(source='code_site_code_site', write_only=True,label='Code du site')
    code_cient = serializers.CharField(source='code_client_code_client', write_only=True,label='Code du client')

    class Meta:
        model=NT
        fields ='__all__'

    def create(self, validated_data):
        code_site = validated_data.pop('code_site_code_site')
        code_cient = validated_data.pop('code_client_code_client')

        site_obj = Sites.objects.get(
            code_site=code_site
        )
        client_obj = Clients.objects.get(
            code_client=code_cient
        )

        nt = NT.objects.create(code_client=client_obj,code_site=site_obj, **validated_data)
        return nt
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('id', None)
        fields.pop('deleted_by_cascade', None)
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['code_site'] = instance.code_site.code_site
        return representation



class DQESerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(source='marche_nt_code_site_code_site', write_only=True)
    nt = serializers.CharField(source='marche_nt_nt', write_only=True)
    num_avenant=serializers.CharField(source='marche_num_avenant', write_only=True)
    class Meta:
        model=DQE
        fields='__all__'

    def create(self, validated_data):
        code_site = validated_data.pop('marche_nt_code_site_code_site')
        nt = validated_data.pop('marche_nt_nt')
        num_avenant=validated_data.pop('marche_num_avenant')

        marche_obj = Marche.objects.get(
            nt__nt=nt,
            nt__code_site__code_site=code_site,
            num_avenant=num_avenant
        )
        dqe = DQE.objects.create(marche=marche_obj, **validated_data)
        return dqe

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('id', None)
        fields.pop('marche', None)
        fields.pop('deleted_by_cascade', None)
        return fields


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prix_q'] = instance.prix_q
        representation['code_site'] = instance.marche.nt.code_site.code_site
        representation['nt'] = instance.marche.nt.nt
        representation['avenant'] = instance.marche.num_avenant

        return representation





class MarcheSerializer(serializers.ModelSerializer):
    code_site = serializers.CharField(source='nt_code_site_code_site',write_only=True,label='Code du site')
    nt = serializers.CharField(source='nt_nt',write_only=True,label='Numero du travail')

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





