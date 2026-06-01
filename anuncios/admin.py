from django.contrib import admin
from .models import AnuncioPequeno, AnuncioGrande , AnuncioFlotante



@admin.register(AnuncioPequeno)
class AnuncioPequenoAdmin(admin.ModelAdmin):
    list_display  = ("titulo", "activo", "orden", "fecha_inicio", "fecha_fin")
    list_editable = ("activo", "orden")
    list_filter   = ("activo",)


@admin.register(AnuncioGrande)
class AnuncioGrandeAdmin(admin.ModelAdmin):
    list_display  = ("__str__", "activo", "orden", "fecha_inicio", "fecha_fin","fecha_limite")
    list_editable = ("activo", "orden")
    list_filter   = ("activo",)
    
    
@admin.register(AnuncioFlotante)
class AnuncioFlotanteAdmin(admin.ModelAdmin):
    list_display  = ('id', 'enlace', 'activo', 'orden', 'fecha_inicio', 'fecha_fin')
    list_editable = ('activo', 'orden')
    list_filter   = ('activo',)