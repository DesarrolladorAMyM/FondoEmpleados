from django.contrib import admin
from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):

    # COLUMNAS QUE SE VEN EN LA LISTA
    list_display = [
        'Nombre',
        'Empresa',
        'Correo',
        'Telefono',
        'Servicio',
        'Fecha_envio',
    ]

    # CAMPOS POR LOS QUE PUEDES BUSCAR 
    search_fields = [
        'Nombre',
        'Empresa',
        'Correo',
        'Servicio',
    ]

    #FILTROS EN LA BARRA LATERAL DERECHA
    list_filter = [
        'Servicio',
        'Fecha_envio',
    ]

    # ORDEN POR DEFECTO 
    ordering = ['-Fecha_envio']

    # CAMPOS DE SOLO LECTURA
    readonly_fields = ['Fecha_envio']

    #CÓMO SE VE EL FORMULARIO DE DETALLE 
    fieldsets = (
        ('Datos de Contacto', {
            'fields': (
                'Nombre',
                'Empresa',
                'Correo',
                'Telefono',
                'Servicio',
            )
        }),
        ('Mensaje', {
            'fields': (
                'Mensaje',
            )
        }),
        ('Fecha', {
            'fields': (
                'Fecha_envio',
            )
        }),
    )