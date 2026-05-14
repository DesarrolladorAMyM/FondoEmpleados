from django.contrib import admin
from django.utils.html import format_html
from .models import Banner,MensajeContacto


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preview_imagen', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_display_links = ['titulo']

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:6px; object-fit:cover; width:120px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    preview_imagen.short_description = "Vista previa"
    
    
    
    

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    
    list_display = ('Nombre', 'Empresa', 'Correo', 'Telefono', 'Servicio', 'Fecha_envio')
    list_filter = ('Servicio', 'Fecha_envio')
    search_fields = ('Nombre', 'Empresa', 'Correo')
    ordering = ('-Fecha_envio',)
    
    readonly_fields = ('Nombre', 'Empresa', 'Correo', 'Telefono', 'Servicio', 'Mensaje', 'Fecha_envio')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False