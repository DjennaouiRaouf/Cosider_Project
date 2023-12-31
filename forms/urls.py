from django.urls import path
from .views import *

urlpatterns = [

    path('userfields/', UserFieldsApiView.as_view()),
    path('userfieldsstate/', UserFieldsStateApiView.as_view()),

    path('clientfilterfields/',ClientFieldsFilterApiView.as_view()),
    path('clientfields/', ClientFieldsApiView.as_view()),
    path('clientfieldsstate/', ClientFieldsStateApiView.as_view()),

    path('marchefilterfields/',MarcheFieldsFilterApiView.as_view()),
    path('marchefields/', MarcheFieldsApiView.as_view()),
    path('marchefieldsstate/',MarcheFieldsStateApiView.as_view()),

    path('sitefilterfields/',SiteFieldsFilterApiView.as_view()),
    path('sitefields/', SiteFieldsApiView.as_view()),
    path('sitefieldsstate/',SiteFieldsStateApiView.as_view()),

    path('dqefilterfields/',DQEFieldsFilterApiView.as_view()),
    path('dqefields/', DQEFieldsApiView.as_view()),
    path('dqefieldsstate/',DQEFieldsStateApiView.as_view()),

    path('ntfilterfields/',NTFieldsFilterApiView.as_view()),
    path('ntfields/',NTFieldsApiView.as_view()),
    path('ntfieldsstate/',NTFieldsApiView.as_view()),

    path('facturefields/', FactureFieldsApiView.as_view()),
    path('facturefieldsstate/',FactureFieldsStateApiView.as_view()),
    path('facturefilterfields/',FactureFieldsFilterApiView.as_view()),


    path('encaissmentfields/',EncaissementFieldsApiView.as_view()),
    path('encaissementfieldsstate/',EncaissementFieldsStateApiView.as_view()),
    path('encaissementfilterfields/',EncaissementFieldsFilterApiView.as_view()),


]