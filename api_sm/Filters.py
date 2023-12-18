import django_filters

from api_sm.models import *


class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Clients
        fields = ['id', 'type_client',]


class SitesFilter(django_filters.FilterSet):
    class Meta:
        model = Sites
        fields = ['id', 'type_site','code_filiale','code_division','code_commune_site','code_region']


class NTFilter(django_filters.FilterSet):
    class Meta:
        model = NT
        fields=['nt','code_site','code_client']