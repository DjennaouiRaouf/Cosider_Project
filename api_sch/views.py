from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

# Create your views here.
from .Serializers import *
from .models import *
from .Filters import *

class GetProduction(generics.ListAPIView):
    #permission_classes = [IsAuthenticated,ViewODSPermission]
    queryset = TabProduction.objects.all()
    serializer_class = ProductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProdFilter