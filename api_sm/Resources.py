from import_export import resources
from api_sm.models import *

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


class MarcheResource(resources.ModelResource):
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



class DQEResource(resources.ModelResource):
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