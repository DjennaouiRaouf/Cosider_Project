from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from api_sm.Resources import *
from api_sm.models import *



lp=25



'''

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key','src','est_bloquer')
    list_filter = ()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer = not obj.est_bloquer
            obj.save()


'''




@admin.register(Clients)
class ClientAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_per_page = lp
    resource_class=ClientResource
    list_display = ('code_client','type_client','est_client_cosider','nif','raison_social','user_id','date_modification')
    list_filter = (
        'est_client_cosider',
        'type_client',
    )
    search_fields = ('code_client','nif')



    def save_model(self, request, obj, form, change):
        obj.date_modification=datetime.now()
        super().save_model(request, obj, form, change)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            
            obj.date_modification = datetime.now()
            obj.save()




@admin.register(Sites)
class SitesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = SiteResource
    list_per_page = lp
    list_display = ('code_site','code_filiale','code_region','libelle_site','type_site','code_division',
        'code_commune_site','date_ouverture_site', 'date_cloture_site','user_id', 'date_modification')
    list_editable = ()

    def save_model(self, request, obj, form, change):
        
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.date_modification = datetime.now()
            obj.save()



@admin.register(Marche)
class MarcheAdmin(ImportExportModelAdmin,admin.ModelAdmin):

    resource_class = MarcheResource
    list_display = ('nt','num_avenant','libelle' ,'ods_depart' ,'delais','ht' ,'ttc' ,'revisable','retenue_de_garantie' ,'rabais'
    ,'tva','user_id','date_modification')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "avenant_du_contrat":

            kwargs["queryset"] = Marche.objects.filter(
                avenant_du_contrat=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        
        obj.date_modification = datetime.now()

        super().save_model(request, obj, form, change)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.save()


@admin.register(NT)
class NTAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = NTResource
    list_display = (
    'code_site','nt','code_client','libelle_nt','date_ouverture_nt','date_cloture_nt','user_id'
    ,'date_modification')

    def save_model(self, request, obj, form, change):
        
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.save()



@admin.register(Ordre_De_Service)
class ODS(ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = ODSResource
    list_display = ("marche","date_interruption","date_reprise","motif","user_id","date_modification")






@admin.register(DQE)
class DQEAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    save_as = True
    resource_class = DQEResource
    list_display = ("marche","designation","unite","quantite","prix_u","prix_q","user_id","date_modification")
    list_editable = ("prix_u",)


@admin.register(TypeAvance)
class  TypeAvanceAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeAvanceResource
    list_display = ("id", "libelle", "user_id","date_modification")

    def save_model(self, request, obj, form, change):
        
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.save()




@admin.register(TypeCaution)
class  TypeCautionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = TypeCautionResource
    list_display = ("id", "libelle", "taux","user_id","date_modification")

    def save_model(self, request, obj, form, change):
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)




@admin.register(Banque)
class BanqueAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = BanqueResource
    list_display = ( "nom", "adresse", "ville", "wilaya","user_id","date_modification")

    def save_model(self, request, obj, form, change):
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)




@admin.register(Cautions)
class CautionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = BanqueResource
    list_display = ("marche", "Type_Caution","montant", "date_soumission", "montant","user_id","date_modification","est_recupere")
    actions = ['recuperer']

    def recuperer(self, request, queryset):
        queryset.update(est_recupere=True)
    def Type_Caution(self,obj):
        return obj.type.libelle

    def save_model(self, request, obj, form, change):
        obj.date_modification = datetime.now()
        super().save_model(request, obj, form, change)


@admin.register(Attachements)
class AttachementAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=("marche","designation","qte_realise","avancement","montant_estime",'montant_rg','montant_rb','montant_final')


    def avancement(self,obj):
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            obj.taux
        )
    def marche(self,obj):
        return obj.dqe.marche

    def designation(self, obj):
        return obj.dqe.designation



@admin.register(Factures)
class FacturesAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('numero_facture','date_facture','montant_global',
                    'etat')

    def etat(self, obj):
        return obj.etat_de_facture


@admin.register(DetailFacture)
class DetailFactureAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("numero_facture","detail_designation","detail_estimation","detail_montant_rg","detail_montant_rb","detail_montant")

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


@admin.register(Encaissement)
class Encaissement(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('numero_facture','date_encaissement','mode_paiement','montant_encaisse','montant_creance')
    def numero_facture(self, obj):
        return obj.facture.numero_facture
