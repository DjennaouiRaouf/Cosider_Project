from django.urls import path
from .views import *

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('whoami/', WhoamiView.as_view()),
    path('ic_images/', GetICImages.as_view()),
    path('addclient/',AjoutClientApiView.as_view()),
    path('getclients/', GetClientsView.as_view()),
    path('clientfields/',ClientFieldsApiView.as_view()),
    path('marchefields/',MarcheFieldsApiView.as_view()),
    path('sitefields/', SiteFieldsApiView.as_view()),
    path('addsite/',AjoutSiteApiView.as_view()),
    path('getsites/', GetSitesView.as_view()),
    path('addmarche/',AjoutMarcheApiView.as_view()),
    path('getmarche/',GetMarcheView.as_view()),
    path('adddqe/',AddDQEView.as_view()),
    path('getdqe/', GetDQEView.as_view()),



]