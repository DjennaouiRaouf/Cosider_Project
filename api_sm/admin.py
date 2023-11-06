from django.contrib import admin
from api_sm.models import *



lp=25


class ImagesAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = ('key','src','visible',)
    list_filter = ('visible',)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.visible=False
            obj.save()

admin.site.register(Images, ImagesAdmin)





class ClientAdmin(admin.ModelAdmin):
    list_per_page = lp
    list_display = ('code_client','type_client','est_client_cosider','nif','raison_social','user_id','date_modification','est_bloquer')
    list_filter = ('est_bloquer','est_client_cosider','type_client')
    search_fields = ('code_client','nif')
    list_editable = ('est_bloquer',)


    def save_model(self, request, obj, form, change):

        obj.user_id = User.objects.get(id=request.user.id)

        super().save_model(request, obj, form, change)
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.est_bloquer=False
            obj.save()

admin.site.register(Clients, ClientAdmin)