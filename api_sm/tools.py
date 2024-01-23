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
