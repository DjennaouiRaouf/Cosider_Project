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