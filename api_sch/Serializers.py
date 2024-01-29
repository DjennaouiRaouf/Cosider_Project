from rest_framework import serializers

from api_sch.models import *
class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TabProduction
        fields='__all__'


    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields.pop('deleted', None)
        fields.pop('user_id', None)
        fields.pop('date_modification', None)
        fields.pop('est_cloturer', None)
        fields.pop('prevu_realiser', None)
        fields.pop('deleted_by_cascade', None)

        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['valeur_1'] = round(instance.valeur_1,2)
        representation['quantite_1'] = round(instance.quantite_1,2)
        representation['valeur_2'] = round(instance.valeur_2,2)
        representation['quantite_2'] = round(instance.quantite_2,2)
        representation['valeur_3'] = round(instance.valeur_3,2)
        representation['quantite_3'] = round(instance.quantite_3,2)

        return representation


