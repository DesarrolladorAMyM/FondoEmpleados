from django.contrib import admin
from .models import Anuncio

# Register your models here.
@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display  = ("titulo", "activo", "orden", "fecha_inicio", "fecha_fin")
    list_editable = ("activo", "orden")
    list_filter   = ("activo",)