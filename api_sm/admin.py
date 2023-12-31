
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.humanize.templatetags import humanize
from django.utils.html import format_html
from django_admin_relation_links import AdminChangeLinksMixin
from djangoql.admin import DjangoQLSearchMixin
from import_export.admin import ImportExportModelAdmin, ExportMixin
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


@admin.register(OptionImpression)
class OptionImpressionAdmin(SafeDeleteAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key', 'src','type')


@admin.register(Images)
class ImagesAdmin(SafeDeleteAdmin,admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key','src')
    list_filter = ()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer = not obj.est_bloquer
            obj.save()



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

@admin.register(NT)
class NTAdmin(AdminChangeLinksMixin,SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = NTResource
    list_display = (
    'nt','code_client_link','code_site_link','libelle','date_ouverture_nt','date_cloture_nt',
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
    list_display = ('id',"marche","code_tache","libelle","unite","quantite","prix_unitaire","prix_quntite",)
    history_list_display = ("marche","code_tache","libelle",'unite',"quantite","prix_unitaire","prix_quntite",)
    list_filter = (SafeDeleteAdminFilter,

                   )
    search_fields = ('marche__id',)

    def num_avenant(self,obj):
        return obj.marche.num_avenant

    def prix_unitaire(self,obj):
        return humanize.intcomma(obj.prix_u)

    prix_unitaire.short_description="Prix unitaire"
    def prix_quntite(self,obj):
        return humanize.intcomma(obj.prix_q)
    prix_quntite.short_description = "Prix quantite"


    def id(self,obj):
        return obj.marche.nt.id
    def numero_t(self,obj):
        return  obj.marche.nt.nt

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
    history_list_display = ('nt','libelle' ,'ods_depart' ,'delais','pht' ,'pttc' ,'revisable','rg' ,'rabais'
    ,'tva','date_signature')
    list_display = ('id','nt_link','libelle' ,'ods_depart' ,'delais','pht' ,'pttc' ,'revisable','rg' ,'rabais'
    ,'tva','date_signature')


    list_filter = (SafeDeleteAdminFilter,

                   )
    search_fields = ('nt__nt','id')
    change_links = ('nt',)

    def pht(self,obj):
        return humanize.intcomma(obj.ht)

    pht.short_description = 'HT'

    def pttc(self, obj):
        return humanize.intcomma(obj.ttc)

    pttc.short_description = 'TTC'

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

 

@admin.register(Avance)
class  AvanceAdmin(SafeDeleteAdmin,SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    resource=AvanceResource
    list_display = ("marche", "type","montant_avance","client" )
    list_filter = (SafeDeleteAdminFilter,)

    def montant_avance(self,obj):
        return humanize.intcomma(obj.montant)
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
    list_display = ( "nom", "adresse", "ville", "wilaya","libelle")
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
    list_display=("dqe",'qte_contr',"qte_precedente","qte_mois","qte_cumule","prix_u","montant_prec",'montant_m','montant_c','date','heure')
    list_filter = (SafeDeleteAdminFilter,)

    def prix_u(self,obj):
        return humanize.intcomma(obj.dqe.prix_u)
    def qte_contr(self,obj):
        return obj.dqe.quantite
    def montant_prec(self,obj):
        return humanize.intcomma(obj.montant_precedent)
    def montant_m(self,obj):
        return humanize.intcomma(obj.montant_mois)
    def montant_c(self,obj):
        return humanize.intcomma(obj.montant_cumule)


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
    list_display = ('numero_facture','num_situation','du','au',"montant_prec",'montant_m','montant_c','date',"heure",
                    'etat')
    list_filter = (SafeDeleteAdminFilter,)
    def montant_prec(self,obj):
        return humanize.intcomma(obj.montant_precedent)
    def montant_m(self,obj):
        return humanize.intcomma(obj.montant_mois)
    def montant_c(self,obj):
        return humanize.intcomma(obj.montant_cumule)
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
class DetailFactureAdmin(SimpleHistoryAdmin,ExportMixin,admin.ModelAdmin):
    list_display = ("numero_facture","code_tache","detail_designation","montant_precedent","montant_mois"
                    ,"montant_cumule")


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
        return False
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def montant_precedent(self,obj):
        return humanize.intcomma(obj.detail.montant_precedent)
    def montant_mois(self,obj):
        return humanize.intcomma(obj.detail.montant_mois)
    def montant_cumule(self,obj):
        return humanize.intcomma(obj.detail.montant_cumule)

    def numero_facture(self, obj):
        return obj.facture.numero_facture
    def detail_designation(self,obj):
        return obj.detail.dqe.libelle

    def code_tache(self,obj):
        return obj.detail.dqe.code_tache


    def detail_montant_rg(self, obj):
        return obj.detail.montant_rg
    def detail_montant_rb(self, obj):
        return obj.detail.montant_rb
    def detail_montant(self, obj):
        return obj.detail.montant_final



class EncaissementAmin(SafeDeleteAdmin,SimpleHistoryAdmin,admin.ModelAdmin):

    list_display = ('numero_facture','date_encaissement','mode_paiement','montant_facture','encaisse','creance')
    save_as = True
    list_filter = (SafeDeleteAdminFilter,)

    def montant_facture(self,obj):
        return humanize.intcomma(obj.facture.a_payer)

    def encaisse(self, obj):
        return humanize.intcomma(obj.montant_encaisse)

    def creance(self, obj):
        return humanize.intcomma(obj.montant_creance)


    def has_change_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return super().has_change_permission(request, obj)


    def numero_facture(self, obj):
        return obj.facture.numero_facture


admin.site.register(Encaissement, EncaissementAmin)


@admin.register(ModePaiement)
class ModePaiementAdmin(SimpleHistoryAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("id","libelle")
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