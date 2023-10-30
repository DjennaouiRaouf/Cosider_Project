from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('ic_images/', GetICImages.as_view()),
    path('addclient/',AddClientView.as_view()),

]