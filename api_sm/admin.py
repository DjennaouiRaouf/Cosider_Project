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