from django.urls import path
from .views import *

urlpatterns = [
    path('ic_images/', GetICImages.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('whoami/',WhoamiView.as_view()),
    path('session/',SessionIDView.as_view()),





]