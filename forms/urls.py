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
    path('dfacture/',DetailFactureFieldsApiView.as_view()),
    path('dfacturefilterfields/',DetailFactureFieldsFilterApiView.as_view()),

    path('avancefields/',AvanceFieldsApiView.as_view()),
    path('avancefieldsstate/',AvanceFieldsStateApiView.as_view()),


    path('cautionfields/',CautionFieldsApiView.as_view()),
    path('cautionfieldsstate/',CautionFieldsStateApiView.as_view()),
    path('flashfields/',FlashFieldsApiView.as_view()),

    path('odsfields/',ODSFieldsApiView.as_view()),
    path('odsfieldsstate/',OdsFieldsStateApiView.as_view()),
    path('odsfilterfields/',OdsFieldsFilterApiView.as_view()),

]