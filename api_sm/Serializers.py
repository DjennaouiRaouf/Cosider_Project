from rest_framework import serializers
from api_sm.models import *

def create_dynamic_serializer(model_class):
    class DynamicModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    return DynamicModelSerializer
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
    class Meta:
        model=NT
        fields ='__all__'
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('id', None)
        fields.pop('deleted_by_cascade', None)
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation



class DQESerializer(serializers.ModelSerializer):
    code_marche= serializers.CharField(source='marche_code_marche',write_only=True,label='Code du marché')
    class Meta:
        model=DQE
        fields='__all__'

    def create(self, validated_data):
        code_marche = validated_data.pop('marche_code_marche')


        marche_obj = Marche.objects.get(
            code_marche=code_marche
        )

        nt = DQE.objects.create(marche=marche_obj, **validated_data)
        return nt

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('id', None)
        fields.pop('marche', None)
        fields.pop('deleted_by_cascade', None)
        fields.pop('prix_q', None)

        return fields


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prix_q'] = instance.prix_q
        representation['code_site'] = instance.marche.nt.code_site.code_site
        representation['nt'] = instance.marche.nt.nt
        representation['code_marche'] = instance.marche.nt.nt
        representation['avenant'] = instance.marche.num_avenant


        return representation





class MarcheSerializer(serializers.ModelSerializer):


    class Meta:
        model = Marche
        fields = "__all__"

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





