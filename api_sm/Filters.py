import django_filters

from api_sm.models import *


class NTFilter(django_filters.FilterSet):
    class Meta:
        model = NT
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.filters['deleted']
        del self.filters['deleted_by_cascade']
