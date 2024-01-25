import django_filters
from django.db.models import Q

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
    code_site = django_filters.ModelChoiceFilter(field_name='nt__code_site', label='Code du site',
                                                 queryset=Sites.objects.all(),)
    code_contrat = django_filters.CharFilter(field_name='code_contrat', label='Code du contrat')
    date_signature=django_filters.DateFilter(field_name="date_signature",label='Date de signature')
    nt = django_filters.CharFilter(field_name='nt__nt', label='Numero du travail')
    rabais=django_filters.NumberFilter(field_name='rabais', label='Rabais')
    tva = django_filters.NumberFilter(field_name='tva', label='TVA')
    rg = django_filters.NumberFilter(field_name='rg', label='Retenue de garantie')
    client=django_filters.BooleanFilter(field_name='nt__code_client__est_client_cosider', label='Cosider client')


    class Meta:
        model = Marche
        fields=['code_contrat','date_signature','rabais','code_site','nt','tva','rg','client']


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

class DetailFactureFilter(django_filters.FilterSet):
    code_tache = django_filters.CharFilter(field_name='detail__dqe__code_tache', lookup_expr='icontains',label="Code Tache")
    libelle_tache = django_filters.CharFilter(field_name='detail__dqe__libelle', lookup_expr='icontains',label="Libelle")

    class Meta:
        model = DetailFacture
        fields = ['facture','code_tache','libelle_tache' ]


class AvanceFilter(django_filters.FilterSet):

    class Meta:
        model = Avance
        fields=['marche',]


class CautionFilter(django_filters.FilterSet):

    class Meta:
        model = Cautions
        fields=['marche',]

class Ordre_De_ServiceFilter(django_filters.FilterSet):

    class Meta:
        model = Ordre_De_Service
        fields=['marche','date_interruption','date_reprise']


class TypeAvanceFilter(django_filters.FilterSet):
    class Meta:
        model = TypeAvance
        fields=['id',]


class TypeCautionFilter(django_filters.FilterSet):
    class Meta:
        model = TypeCaution
        fields=['id',]