
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('admin/', admin.site.urls),
    path('sm/',include('api_sm.urls')),
    path('sch/', include('api_sch.urls')),
    path('forms/',include('forms.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)