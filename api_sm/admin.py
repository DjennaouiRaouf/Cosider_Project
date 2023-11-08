from datetime import datetime
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api_sm.Resources import *
from api_sm.models import *



lp=25


class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key','src','est_bloquer',)
    list_filter = ('est_bloquer',)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer= not obj.est_bloquer
            obj.save()

admin.site.register(Images, ImagesAdmin)





class ClientAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    resource_class=ClientResource
    list_display = ('code_client','type_client','est_client_cosider','nif','raison_social','user_id','date_modification','est_bloquer')
    list_filter = (
        'est_bloquer',
        'est_client_cosider',
        'type_client',
    )
    search_fields = ('code_client','nif')
    list_editable = ('est_bloquer',)


    def save_model(self, request, obj, form, change):

        obj.user_id = User.objects.get(id=request.user.id)
        obj.date_modification=datetime.now()
        super().save_model(request, obj, form, change)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer= not obj.est_bloquer
            obj.date_modification = datetime.now()
            obj.save()

admin.site.register(Clients, ClientAdmin)



class SitesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('code_site','code_filiale','code_region','libelle_site','type_site','code_division',
        'code_commune_site','date_ouverture_site', 'date_cloture_site','user_id', 'est_bloquer','date_modification')
    list_editable = ('est_bloquer',)

    def save_model(self, request, obj, form, change):
        obj.user_id = User.objects.get(id=request.user.id)
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer= not obj.est_bloquer
            obj.date_modification = datetime.now()
            obj.save()

admin.site.register(Sites, SitesAdmin)


class MarcheAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = MarcheResource
    list_display = ('nt','avenant','libelle' ,'ods_depart' ,'delais','ht' ,'ttc' ,'revisable' ,'rabais'
    ,'tva','user_id','date_modification')
    def save_model(self, request, obj, form, change):
        obj.user_id = User.objects.get(id=request.user.id)
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)

admin.site.register(Marche, MarcheAdmin)

class NTAdmin(admin.ModelAdmin):
    list_display = (
    'code_site','nt','code_client','libelle_nt','date_ouverture_nt','date_cloture_nt','est_bloquer','user_id'
    ,'date_modification')

    def save_model(self, request, obj, form, change):
        obj.user_id = User.objects.get(id=request.user.id)
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer = not obj.est_bloquer
            obj.date_modification = datetime.now()
            obj.save()

admin.site.register(NT, NTAdmin)

class DQEAdmin(admin.ModelAdmin):
    list_display = ("marche","designation","prix_u","unite","quantite","prix_q")

admin.site.register(DQE, DQEAdmin)
