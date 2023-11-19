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
        fields= "__all__"






class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class DQESerializer(serializers.ModelSerializer):
    class Meta:
        model=DQE
        fields='__al__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prix_q'] = instance.prix_q
        return representation

class ListMarcheSerializer(serializers.ModelSerializer):
    nt = NTSerializer()
    avenants= RecursiveSerializer(many=True)
    class Meta:
        model=Marche
        fields="__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ht'] = instance.ttc
        representation['ttc'] = instance.ttc
        return representation




