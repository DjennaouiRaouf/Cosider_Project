from rest_framework import serializers
from .models import *



class ICSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interface_de_Connexion
        fields = '__all__'