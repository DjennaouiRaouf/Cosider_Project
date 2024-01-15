
from decimal import Decimal
from _decimal import InvalidOperation
from django.contrib.humanize.templatetags import humanize
from django.db import transaction
from import_export import resources, fields
from import_export.widgets import Widget
from api_sm.models import *


class FormattedPriceWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            cleaned_value = value.replace(',', '.').replace('\xa0', '')

            return Decimal(cleaned_value)
        except (ValueError, InvalidOperation) as e:
            print(f"Erreur de conversion de la valeur ({value}) en decimal: {e}")
            return None


    def render(self, value, obj=None):
        return humanize.intcomma(value)

class TabUniteDeMesureResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = TabUniteDeMesure
        exclude =('deleted','deleted_by_cascade')

class UserResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = User

class ClientResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Clients
        exclude =('deleted','deleted_by_cascade')


class SiteResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Sites
        exclude = ('deleted', 'deleted_by_cascade')


class MarcheResource(resources.ModelResource):
    ttc = fields.Field(column_name='ttc', attribute='ttc', widget=FormattedPriceWidget())
    ht = fields.Field(column_name='ht', attribute='ht', widget=FormattedPriceWidget())
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Marche
        exclude = ('code_marche','deleted', 'deleted_by_cascade')


class ODSResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Ordre_De_Service
        exclude = ('deleted', 'deleted_by_cascade')



class DQEResource(resources.ModelResource):
    prix_u = fields.Field(column_name='prix_u', attribute='prix_u', widget=FormattedPriceWidget())
    prix_q = fields.Field(column_name='prix_q', attribute='prix_q', widget=FormattedPriceWidget())
    annule = fields.Field(column_name='annule', attribute=None)
    def dehydrate_annule(self, obj):
        return f"0"
    def before_export(self, queryset, *args, **kwargs):
        for obj in queryset:
            setattr(obj, 'annule', '0')
    def skip_row(self, instance, original, row, import_validation_errors=None):
        if(row.get('annule') == 1):
            DQE.objects.get(id=row.get('id')).delete()
            return True
        if(row.get('annule') == None):
                return  False


    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None

    class Meta:
        model = DQE
        exclude = ('deleted', 'deleted_by_cascade')



class AvanceResource(resources.ModelResource):
    montant = fields.Field(column_name='montant', attribute='montant', widget=FormattedPriceWidget())

    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = DQE
        exclude = ('id','deleted', 'deleted_by_cascade')

class NTResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = NT
        exclude = ('deleted', 'deleted_by_cascade')

class TypeAvanceResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = TypeAvance
        exclude = ('deleted', 'deleted_by_cascade')


class TypeCautionResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = TypeCaution
        exclude = ('deleted', 'deleted_by_cascade')

class BanqueResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Banque
        exclude = ('deleted', 'deleted_by_cascade')

class AgenceResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Agence
        exclude = ('deleted', 'deleted_by_cascade')

class CautionResource(resources.ModelResource):
    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in instance_loader.resource.get_import_id_fields():
                field = instance_loader.resource.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
    class Meta:
        model = Cautions
        exclude = ('deleted', 'deleted_by_cascade')