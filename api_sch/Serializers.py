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

