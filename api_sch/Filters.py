import django_filters
from django.db.models import Q
from django.db.models.functions import ExtractMonth, ExtractYear

from api_sch.models import *
class ProdFilter(django_filters.FilterSet):
    mm = django_filters.NumberFilter(field_name='mmaa__month', label='Mois')
    aa = django_filters.NumberFilter(field_name='mmaa__year', label='Année')

    class Meta:
        model = TabProduction
        fields = ['code_site','prevu_realiser','nt','code_type_production']

