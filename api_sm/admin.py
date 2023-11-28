from adminfilters.autocomplete import AutoCompleteFilter
from adminfilters.combo import ChoicesFieldComboFilter
from adminfilters.dj import DjangoLookupFilter
from adminfilters.mixin import AdminFiltersMixin
from adminfilters.numbers import NumberFilter
from adminfilters.querystring import QueryStringFilter
from adminfilters.radio import RelatedFieldRadioFilter
from adminfilters.value import ValueFilter
from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter
from simple_history.admin import SimpleHistoryAdmin
from api_sm.Resources import *
from api_sm.models import *



lp=25



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




@admin.register(Clients)
class ClientAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    resource_class=ClientResource
    list_display = ('code_client','type_client','est_client_cosider','nif','raison_social',)
    list_filter = (
        'est_client_cosider',
        'type_client',
        SafeDeleteAdminFilter
    )
    search_fields = ('code_client','nif')
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)







@admin.register(Sites)
class SitesAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = SiteResource
    list_per_page = lp
    list_display = ('code_site','code_filiale','code_region','libelle_site','type_site','code_division',
        'code_commune_site','date_ouverture_site', 'date_cloture_site', )
    list_editable = ()
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)





@admin.register(Marche)
class MarcheAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = MarcheResource
    list_display = ('nt','num_avenant','libelle' ,'ods_depart' ,'delais','ht' ,'ttc' ,'revisable','retenue_de_garantie' ,'rabais'
    ,'tva',)

    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "avenant_du_contrat":

            kwargs["queryset"] = Marche.objects.filter(
                avenant_du_contrat=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(NT)
class NTAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = NTResource
    list_display = (
    'code_site','nt','code_client','libelle_nt','date_ouverture_nt','date_cloture_nt',
    )
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)






@admin.register(Ordre_De_Service)
class ODS(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = ODSResource
    list_display = ("marche","date_interruption","date_reprise","motif",)
    list_filter = (SafeDeleteAdminFilter,)

    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)




@admin.register(DQE)
class DQEAdmin(AdminFiltersMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as=True
    resource_class = DQEResource
    list_display = ("marche","designation","unite","quantite","prix_u","prix_q",)
    list_filter = ("designation",
                   #("marche__nt__code_site__code_site",ValueFilter.factory(lookup_name='exact')),
                   #("marche__nt__nt", ValueFilter.factory(lookup_name='exact')),
                   #("marche__num_avenant",ValueFilter.factory(lookup_name='exact') ),
                   )

    list_editable = ('prix_u'),


    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)


@admin.register(TypeAvance)
class  TypeAvanceAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeAvanceResource
    list_display = ("id", "libelle", )
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)





@admin.register(TypeCaution)
class  TypeCautionAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeCautionResource
    list_display = ("id", "libelle", "taux",)
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)








@admin.register(Banque)
class BanqueAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = BanqueResource
    list_display = ( "nom", "adresse", "ville", "wilaya",)
    list_filter = (SafeDeleteAdminFilter,)

    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)




@admin.register(Cautions)
class CautionAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = BanqueResource
    list_display = ("marche", "Type_Caution","montant", "date_soumission", "montant","est_recupere")
    actions = ['recuperer']
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)


    def recuperer(self, request, queryset):
        queryset.update(est_recupere=True)
    def Type_Caution(self,obj):
        return obj.type.libelle

    def save_model(self, request, obj, form, change):
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)


@admin.register(Attachements)
class AttachementAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    list_display=("dqe","qte_realise","qte_rest","avancement","montant_estime",'montant_rg','montant_rb','montant_final'
                  ,)
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
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
    list_display = ('numero_facture','date_facture','montant_global',
                    'etat')
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def etat(self, obj):
        if obj.etat_de_facture == True:
            return format_html(
                '''
               <img src="/static/admin/img/icon-yes.svg" alt="True">
                '''
            )
        if obj.etat_de_facture == False:
            return format_html(
                '''
               <img src="/static/admin/img/icon-no.svg" alt="False">
                '''
            )


@admin.register(DetailFacture)
class DetailFactureAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("numero_facture","detail_designation","detail_estimation","detail_montant_rg","detail_montant_rb","detail_montant")
    list_filter = (SafeDeleteAdminFilter,)
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def numero_facture(self, obj):
        return obj.facture.numero_facture
    def detail_designation(self,obj):
        return obj.detail.dqe.designation

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
    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)

    def numero_facture(self, obj):
        return obj.facture.numero_facture
    def montant_facture(self,obj):

        return obj.facture.montant_global

admin.site.register(Encaissement, EncaissementAmin)