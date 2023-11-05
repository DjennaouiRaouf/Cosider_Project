from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('whoami/', WhoamiView.as_view()),
    path('ic_images/', GetICImages.as_view()),
    path('addclient/',AddClientView.as_view()),
    path('getclients/', GetClientsView.as_view()),
    path('addsite/',AddSiteView.as_view()),
    path('getsites/', GetSitesView.as_view()),

]