import django_filters

from api_sm.models import *


class ClientsFilter(django_filters.FilterSet):
    class Meta:
        model = Clients
        fields = ['id','type_client','est_client_cosider']


class SitesFilter(django_filters.FilterSet):
    class Meta:
        model = Sites
        fields = ['id', 'type_site','code_filiale','code_division','code_commune_site','code_region']


class NTFilter(django_filters.FilterSet):
    class Meta:
        model = NT
        fields=['nt','code_site','code_client',]

class MarcheFilter(django_filters.FilterSet):
    code_site = django_filters.CharFilter(field_name='nt__code_site', label='Code du site')
    nt = django_filters.CharFilter(field_name='nt__nt', label='Numero du travail')

    class Meta:
        model = Marche
        fields=['code_contrat','date_signature',]


class DQEFilter(django_filters.FilterSet):
    class Meta:
        model = DQE
        fields=['marche__id','code_tache']

class FactureFilter(django_filters.FilterSet):
    class Meta:
        model = Factures
        fields=['marche','numero_facture','paye']

class EncaissementFilter(django_filters.FilterSet):
    class Meta:
        model = Encaissement
        fields=['date_encaissement','mode_paiement','facture']

class UMFilter(django_filters.FilterSet):
    class Meta:
        model = TabUniteDeMesure
        fields=['id',]

class MPFilter(django_filters.FilterSet):
    class Meta:
        model = ModePaiement
        fields=['id',]