from django.urls import path
from .views import *

urlpatterns = [

    path('adduser/',CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('whoami/', WhoamiView.as_view()),
    path('ic_images/', GetICImages.as_view()),



    path('adddqe/',AjoutDQEApiView.as_view()),
    path('addclient/',AjoutClientApiView.as_view()),
    path('addmarche/', AjoutMarcheApiView.as_view()),
    path('addsite/',AjoutSiteApiView.as_view()),
    path('addnt/',AjoutNTApiView.as_view()),


    path('importdqe/',ImportDQEAPIView.as_view()),
    path('optionimpression/',OptionImpressionApiView.as_view()),


    path('getclients/', GetClientsView.as_view()),

    path('getsites/', GetSitesView.as_view()),

    path('getmarche/',GetMarcheView.as_view()),

    path('getdqe/', GetDQEView.as_view()),
    path('deldqe/',DelDQEByID.as_view()),
    path('deleteddqe/',DeletedDQE.as_view()),
    path('updatedqe/<str:pk>/',UpdateDQEApiVew.as_view()),

    path('getnt/',GetNTView.as_view()),
    path('getmdqe/<str:marche>/',GetDQEbyId.as_view()),



    path('addfacture/',AddFactureApiView.as_view()),
    path('getfacture/',GetFacture.as_view()),
    path('getfacturerg/',GetFactureRG.as_view()),

    path('encaisser/',AddEncaissement.as_view()),
    path('encaissements/',GetEncaissement.as_view()),





]