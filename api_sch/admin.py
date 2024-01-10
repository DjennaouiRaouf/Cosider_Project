from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from api_sch.models import *


@admin.register(TabActivite)
class ActiviteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("code_activite", "libelle_activite")

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


@admin.register(TabGroupeactivite)
class ActiviteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("code_groupeactivite", "libelle_groupeactivite")

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


@admin.register(TabGroupeactiviteActivite)
class GroupeactiviteActivite(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("code_groupeactivite", "code_activite")

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


