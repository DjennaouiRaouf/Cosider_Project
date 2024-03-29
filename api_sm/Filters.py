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
    code_contrat = django_filters.CharFilter(field_name='id', label='Code du contrat')
    date_signature=django_filters.DateFilter(field_name="date_signature",label='Date de signature')
    nt = django_filters.CharFilter(field_name='nt__nt', label='Numero du travail')
    rabais=django_filters.NumberFilter(field_name='rabais', label='Rabais')
    tva = django_filters.NumberFilter(field_name='tva', label='TVA')
    rg = django_filters.NumberFilter(field_name='rg', label='Retenue de garantie')
    client=django_filters.BooleanFilter(field_name='nt__code_client__est_client_cosider', label='Cosider client')
    has_rg = django_filters.BooleanFilter(field_name='rg', label='Avec retenue de garantie ?',method='filter_has_rg',)
    has_tva = django_filters.BooleanFilter(field_name='tva', label='Avec TVA ?',method='filter_has_tva',)
    has_rabais = django_filters.BooleanFilter(field_name='rabais', label='Avec Rabais ? ',method='filter_has_rabais',)

    def filter_has_rabais(self, queryset, name, value):
        if value is False:
            return queryset.filter(**{f"{name}__exact": 0})  
        elif value is True:
            return queryset.exclude(**{f"{name}__exact": 0})  
        return queryset
    def filter_has_tva(self, queryset, name, value):
        if value is False:
            return queryset.filter(**{f"{name}__exact": 0})  
        elif value is True:
            return queryset.exclude(**{f"{name}__exact": 0})  
        return queryset
    def filter_has_rg(self, queryset, name, value):
        if value is False:
            return queryset.filter(**{f"{name}__exact": 0})  
        elif value is True:
            return queryset.exclude(**{f"{name}__exact": 0})  
        return queryset
    class Meta:
        model = Marche
        fields=['code_contrat','date_signature','code_site','client','nt','tva','rg','rabais','has_rg','has_tva',]


class DQEFilter(django_filters.FilterSet):
    class Meta:
        model = DQE
        fields=['marche','code_tache']

class FactureFilter(django_filters.FilterSet):
    class Meta:
        model = Factures
        fields=['marche','numero_facture','paye',"is_remb"]

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
        fields=['marche','remboursee']


class CautionFilter(django_filters.FilterSet):

    class Meta:
        model = Cautions
        fields=['marche',]

class Ordre_De_ServiceFilter(django_filters.FilterSet):

    class Meta:
        model = Ordre_De_Service
        fields=['marche','date','rep_int']


class TypeAvanceFilter(django_filters.FilterSet):
    class Meta:
        model = TypeAvance
        fields=['id',]


class TypeCautionFilter(django_filters.FilterSet):
    class Meta:
        model = TypeCaution
        fields=['id',]



class AttachementsFilter(django_filters.FilterSet):
    marche = django_filters.CharFilter(field_name='dqe__marche', label="Marche")
    code_tache = django_filters.CharFilter(field_name='dqe__code_tache', label="Code Tache")
    mm = django_filters.NumberFilter(field_name='date__month', label='Mois')
    aa = django_filters.NumberFilter(field_name='date__year', label='Année')

    class Meta:
        model = Attachements
        fields=['marche',]

class WorkStateFilter(django_filters.FilterSet):
    marche = django_filters.CharFilter(field_name='dqe__marche', label="Marche")
    date = django_filters.DateFromToRangeFilter(field_name='date', label='Date')

    class Meta:
        model = Attachements
        fields=['marche','date']


class OpImpFilter(django_filters.FilterSet):

    class Meta:
        model = OptionImpression
        fields=['type']

class ImageFilter(django_filters.FilterSet):

    class Meta:
        model = Images
        fields=['type']
