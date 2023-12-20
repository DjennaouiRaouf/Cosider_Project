from django.contrib.humanize.templatetags import humanize
from rest_framework import serializers
from api_sm.models import *

def create_dynamic_serializer(model_class):
    class DynamicModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    return DynamicModelSerializer



class UserSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('id', None)
        return fields
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False

        )
        return user


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


class SituationNtSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields


    class Meta:
        model = SituationNt
        fields = '__all__'









class NTSerializer(serializers.ModelSerializer):
    code_site=serializers.PrimaryKeyRelatedField(queryset=Sites.objects.all(),write_only=True,label='Code du site')
    nt = serializers.CharField(write_only=True, label='Numero du travail')
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
        representation['code_site'] = instance.code_site.id
        representation['nt'] = instance.nt

        return representation



class DQESerializer(serializers.ModelSerializer):
    class Meta:
        model=DQE
        fields='__all__'


    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)

        return fields


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        #representation['unite']=instance.unite.libelle
        representation['prix_u']=humanize.intcomma(instance.prix_u)
        representation['prix_q']=humanize.intcomma(instance.prix_q)

        return representation





class MarcheSerializer(serializers.ModelSerializer):
    code_site=serializers.PrimaryKeyRelatedField(source="nt_code_site",queryset=Sites.objects.all(),write_only=True,label='Code du site')
    nt=serializers.CharField(source="nt_nt",write_only=True,label='Numero du travail')
    class Meta:
        model = Marche
        fields = "__all__"



    def create(self, validated_data):
        code_site = validated_data.pop('nt_code_site')
        num_t = validated_data.pop('nt_nt')
        print(code_site,num_t)
        nt_obj = NT.objects.get(
            code_site_id=code_site,
            nt=num_t
        )

        marche = Marche.objects.create(nt=nt_obj, **validated_data)
        return marche

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('deleted_by_cascade', None)
        return fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ht'] = humanize.intcomma(instance.ttc)
        representation['ttc'] = humanize.intcomma(instance.ttc)
        representation['code_site'] = instance.nt.code_site.id
        representation['nt'] = instance.nt.nt
        representation['num_avenant']=instance.num_avenant


        return representation





