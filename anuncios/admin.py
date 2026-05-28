from django.contrib import admin
from .models import AnuncioPequeno, AnuncioGrande


@admin.register(AnuncioPequeno)
class AnuncioPequenoAdmin(admin.ModelAdmin):
    list_display  = ("titulo", "activo", "orden", "fecha_inicio", "fecha_fin")
    list_editable = ("activo", "orden")
    list_filter   = ("activo",)


@admin.register(AnuncioGrande)
class AnuncioGrandeAdmin(admin.ModelAdmin):
    list_display  = ("__str__", "activo", "orden", "fecha_inicio", "fecha_fin")
    list_editable = ("activo", "orden")
    list_filter   = ("activo",)