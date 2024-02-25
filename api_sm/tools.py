from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from decimal import Decimal
from _decimal import InvalidOperation
def unhumanize(value):
    cleaned_value = value.replace(',', '.').replace('\xa0', '')
    return Decimal(cleaned_value)


class AddClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if( not User.objects.get(id=request.user.id).has_perm('api_sm.add_clients')) :
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter un client")
        return True
class ViewClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_clients')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des clients")
        return True



class AddMarchePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.add_marche')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des Marchés")
        return True

class ViewMarchePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_marche')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des Marchés")
        return True





class AddNTPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if( not User.objects.get(id=request.user.id).has_perm('api_sm.add_nt')) :
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter un NT")
        return True
class ViewNTPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_nt')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des NT")
        return True


class AddDQEPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if( not User.objects.get(id=request.user.id).has_perm('api_sm.add_dqe')) :
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter un DQE")
        return True
class ViewDQEPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_dqe')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des DQE")
        return True


class UploadDQEPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.upload_dqe')):
            raise PermissionDenied("Vous n'êtes pas habilité à de charger le dqe")
        return True

class DownloadDQEPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.download_dqe')):
            raise PermissionDenied("Vous n'êtes pas habilité à de telecharger le dqe")
        return True

class DeleteDQEPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.delete_dqe')):
            raise PermissionDenied("Vous n'êtes pas habilité à de supprimer le dqe")
        return True


class AddSitePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if( not User.objects.get(id=request.user.id).has_perm('api_sm.add_sites')) :
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter un site")
        return True


class ViewSitePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_sites')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des sites")
        return True



class AddAvancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.add_avance')):
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter une avance")
        return True

class ViewAvancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_avance')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser  les avances")
        return True





class AddODSPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if( not User.objects.get(id=request.user.id).has_perm('api_sm.add_ordre_de_service')) :
            raise PermissionDenied("Vous n'êtes pas habilité à ajouter un ods")
        return True


class ViewODSPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if ( not User.objects.get(id=request.user.id).has_perm('api_sm.view_ordre_de_service')):
            raise PermissionDenied("Vous n'êtes pas habilité à visualiser la liste des ods")
        return True




from django.core import exceptions
from django.db.models.fields.related import ForeignKey
from django.db.utils import ConnectionHandler, ConnectionRouter

connections = ConnectionHandler()
router = ConnectionRouter()


class SpanningForeignKey(ForeignKey):

    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        # Call the grandparent rather than the parent to skip validation
        super(ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.rel.to, instance=model_instance)
        qs = self.rel.to._default_manager.using(using).filter(
            **{self.rel.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.rel.to._meta.verbose_name, 'pk': value,
                    'field': self.rel.field_name, 'value': value,
                },  # 'pk' is included for backwards compatibility
            )