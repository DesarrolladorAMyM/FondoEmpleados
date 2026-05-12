from django.contrib import admin
from .models import SolicitudActualizacion


@admin.register(SolicitudActualizacion)
class SolicitudActualizacionAdmin(admin.ModelAdmin):

    #COLUMNAS QUE SE VEN EN LA LISTA 
    list_display = [
        'Numero_radicado',
        'P_nombre',
        'P_apellido',
        'Numero_documento',
        'Celular',
        'Fecha_envio',
    ]

    #CAMPOS POR LOS QUE PUEDES BUSCAR
    search_fields = [
        'Numero_radicado',
        'P_nombre',
        'P_apellido',
        'Numero_documento',
        'Correo_registrado',
        'Celular',
    ]

    #FILTROS EN LA BARRA LATERAL DERECHA
    list_filter = [
        'Tipo_documento',
        'Genero',
        'Departamento',
        'Fuentes_recursos',
        'Fuentes_recursos_otro',
        'Declarante_renta',
        'PeP',
        'Fecha_envio',
    ]

    #ORDEN POR DEFECTO 
    ordering = ['-Fecha_envio']

    #CAMPOS DE SOLO LECTURA
    readonly_fields = ['Fecha_envio', 'Numero_radicado']

    # CÓMO SE VE EL FORMULARIO DE DETALLE 
    fieldsets = (
        ('Identificación', {
            'fields': (
                'Numero_radicado',
                'Tipo_documento',
                'Numero_documento',
                'Correo_registrado',
            )
        }),
        ('Datos Personales', {
            'fields': (
                'P_nombre',
                'S_nombre',
                'P_apellido',
                'S_apellido',
                'Fecha_nacimiento',
                'Genero',
                'Celular',
                'Telefono_fijo',
                
            )
        }),
        ('Ubicación', {
            'fields': (
                'Departamento',
                'Ciudad',
                'Direccion',
            )
        }),
        
        ('Información Económica', {
            'fields': (
                'Fuentes_recursos',
                'Fuentes_recursos_otro'
                'Patrimonio',
                'Declarante_renta',
                'PeP',
            )
        }),
        ('Observaciones y Fecha', {
            'fields': (
                'Observaciones',
                'Fecha_envio',
            )
        }),
    )