import django_filters
from django.db.models import Q
from django.db.models.functions import ExtractMonth, ExtractYear

from api_sch.models import *
class ProdFilter(django_filters.FilterSet):
    mm = django_filters.NumberFilter(method='filter_by_month',label='Mois')
    aa = django_filters.NumberFilter(method='filter_by_year',label='Année')

    class Meta:
        model = TabProduction
        fields = ['mm', 'aa','code_site','nt']

    def filter_by_month(self, queryset, name, value):
        return queryset.annotate(month=ExtractMonth('mmaa')).filter(month=value)

    def filter_by_year(self, queryset, name, value):
        return queryset.annotate(year=ExtractYear('mmaa')).filter(year=value)
