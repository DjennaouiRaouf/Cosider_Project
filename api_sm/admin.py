
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django_admin_relation_links import AdminChangeLinksMixin
from djangoql.admin import DjangoQLSearchMixin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter
from simple_history.admin import SimpleHistoryAdmin
from api_sm.Resources import *
from api_sm.models import *



lp=20

class UserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


'''

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key','src')
    list_filter = ()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer = not obj.est_bloquer
            obj.save()


'''


@admin.register(TabUniteDeMesure)
class TabUniteDeMesure(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    resource_class = TabUniteDeMesureResource
    list_display = ('id','libelle','description')

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

@admin.register(Clients)
class ClientAdmin(DjangoQLSearchMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    resource_class=ClientResource
    list_display = ('id','libelle','type_client','est_client_cosider','nif','raison_social','adresse')
    list_filter = (
        SafeDeleteAdminFilter,
    )
    search_fields = ('id','libelle','type_client','est_client_cosider','nif','raison_social','adresse')

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Sites)
class SitesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = SiteResource
    list_per_page = lp
    list_display = ('id','libelle','code_filiale','code_division','code_region',
        'code_commune_site','date_ouverture_site','date_cloture_site' )
    list_editable = ()
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)


    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_delete_permission(request, obj)




@admin.register(SituationNt)
class SituationNTAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        'id', 'libelle'
    )
    list_filter = (SafeDeleteAdminFilter,)

@admin.register(NT)
class NTAdmin(AdminChangeLinksMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = NTResource
    list_display = (
    'nt','code_client_link','code_site_link','libelle_nt','date_ouverture_nt','date_cloture_nt',
    )
    change_links = ['code_client','code_site']
    list_filter = (SafeDeleteAdminFilter,)
    search_fields = ('nt','code_client__id')
    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 






@admin.register(Ordre_De_Service)
class ODS(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = ODSResource
    list_display = ("marche","date_interruption","date_reprise","motif",)
    list_filter = (SafeDeleteAdminFilter,)


    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

@admin.register(DQE)
class DQEAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as=True
    list_per_page = lp
    resource_class = DQEResource
    list_display = ("marche","code_tache","libelle","unite","quantite","prix_u","prix_q",)
    list_filter = (SafeDeleteAdminFilter,

                   )
    search_fields = ('marche__id','marche__num_avenant')

    def unite(self,obj):
        return obj.unite.libelle

    def id(self,obj):
        return obj.marche.nt.id.id
    def numero_t(self,obj):
        return  obj.marche.nt.nt
    def avenant (self,obj):
        return  obj.marche.num_avenant

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_delete_permission(request, obj)






@admin.register(Marche)
class MarcheAdmin(DjangoQLSearchMixin,AdminChangeLinksMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_per_page = lp
    resource_class = MarcheResource
    list_display = ('id','nt_link','num_avenant','libelle' ,'ods_depart' ,'delais','ht' ,'ttc' ,'revisable','rg' ,'rabais'
    ,'tva','date_signature')


    list_filter = (SafeDeleteAdminFilter,

                   )
    search_fields = ('nt__nt','id','num_avenant')
    change_links = ('nt',)


    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)





@admin.register(TypeAvance)
class  TypeAvanceAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeAvanceResource
    list_display = ("id", "libelle","taux_reduction_facture" )
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 





@admin.register(TypeCaution)
class  TypeCautionAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeCautionResource
    list_display = ("id", "libelle", "taux",)
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 








@admin.register(Banque)
class BanqueAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = BanqueResource
    list_display = ( "nom", "adresse", "ville", "wilaya",)
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 




@admin.register(Cautions)
class CautionAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = BanqueResource
    list_display = ("marche", "Type_Caution","montant", "date_soumission", "montant","est_recupere")
    list_filter = (SafeDeleteAdminFilter,)
    existing_actions = list(SafeDeleteAdmin.actions)
    existing_actions.append('recuperer')
    actions = existing_actions

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return True

    def recuperer(self, request, queryset):
        queryset.filter(deleted=None).update(est_recupere=True)


    def Type_Caution(self,obj):
        return obj.type.libelle




@admin.register(Attachements)
class AttachementAdmin(AdminChangeLinksMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_display=("qte_precedente","qte_mois","qte_cumule","montant_precedent",'montant_mois','montant_cumule',)
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 



    def qte_rest(self,obj):
        return (str(obj.qte_restante)+"/"+str(obj.dqe.quantite))
    def avancement(self,obj):
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            obj.taux
        )
    def dqe(self,obj):
        return obj.dqe

    def designation(self, obj):
        return obj.dqe.designation





@admin.register(Factures)
class FacturesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('numero_facture','du','au','montant_global',
                    'etat')
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):

        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 

    def etat(self, obj):
        if obj.paye == True:
            return format_html(
                '''
               <img src="/static/admin/img/icon-yes.svg" alt="True">
                '''
            )
        if obj.paye == False:
            return format_html(
                '''
               <img src="/static/admin/img/icon-no.svg" alt="False">
                '''
            )


@admin.register(DetailFacture)
class DetailFactureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("numero_facture","detail_designation","detail_estimation","detail_montant_rg","detail_montant_rb","detail_montant")
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 

    def numero_facture(self, obj):
        return obj.facture.numero_facture
    def detail_designation(self,obj):
        return obj.detail.dqe.libelle

    def detail_estimation(self, obj):
        return obj.detail.montant_estime
    def detail_montant_rg(self, obj):
        return obj.detail.montant_rg
    def detail_montant_rb(self, obj):
        return obj.detail.montant_rb
    def detail_montant(self, obj):
        return obj.detail.montant_final



class EncaissementAmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):

    list_display = ('numero_facture','date_encaissement','mode_paiement','montant_facture','montant_encaisse','montant_creance')
    save_as = True
    list_filter = (SafeDeleteAdminFilter,)

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

 

    def numero_facture(self, obj):
        return obj.facture.numero_facture
    def montant_facture(self,obj):

        return obj.facture.montant_global

admin.site.register(Encaissement, EncaissementAmin)