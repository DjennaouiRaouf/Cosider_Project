from django.urls import path
from .views import *

urlpatterns = [
    path('getprod/',GetProduction.as_view()),
]