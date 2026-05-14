from django.contrib import admin
from .models import SolicitudActualizacion

@admin.register(SolicitudActualizacion)
class SolicitudActualizacionAdmin(admin.ModelAdmin):

    # Columnas visibles en la lista
    list_display = (
        'Numero_radicado', 'P_nombre', 'P_apellido',
        'Numero_documento', 'Celular', 'Ciudad',
        'Fuentes_recursos', 'Fecha_envio'
    )

    # Filtros laterales
    list_filter = ('Genero', 'Departamento', 'Declarante_renta', 'PeP', 'Fuentes_recursos', 'Año')

    # Barra de búsqueda
    search_fields = ('P_nombre', 'P_apellido', 'Numero_documento', 'Correo_registrado', 'Numero_radicado')

    # Todos los campos como solo lectura
    readonly_fields = (
        'Tipo_documento', 'Numero_documento', 'Correo_registrado',
        'P_nombre', 'S_nombre', 'P_apellido', 'S_apellido',
        'Fecha_nacimiento', 'Genero', 'Celular', 'Telefono_fijo',
        'Departamento', 'Ciudad', 'Direccion',
        'Residencia_fiscal', 'Residencia_fiscal_pais',
        'Patrimonio', 'Declarante_renta', 'PeP', 'Observaciones',
        'Numero_radicado', 'Año', 'Fuentes_recursos',
        'Fuentes_recursos_otro', 'Fecha_envio'
    )

    # Organizar el detalle por secciones
    fieldsets = (
        ('Identificación', {
            'fields': ('Tipo_documento', 'Numero_documento', 'Correo_registrado', 'Numero_radicado', 'Año')
        }),
        ('Datos Personales', {
            'fields': (
                'P_nombre', 'S_nombre', 'P_apellido', 'S_apellido',
                'Fecha_nacimiento', 'Genero', 'Celular', 'Telefono_fijo'
            )
        }),
        ('Ubicación', {
            'fields': ('Departamento', 'Ciudad', 'Direccion', 'Residencia_fiscal', 'Residencia_fiscal_pais')
        }),
        ('Información Financiera', {
            'fields': ('Patrimonio', 'Declarante_renta', 'Fuentes_recursos', 'Fuentes_recursos_otro')
        }),
        ('Otros', {
            'fields': ('PeP', 'Observaciones', 'Fecha_envio')
        }),
    )

    def has_add_permission(self, _request):
        return False

    def has_delete_permission(self, _request, obj=None):
        return False