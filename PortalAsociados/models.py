from django.db import models

class SolicitudActualizacion(models.Model):
    Tipo_documento        = models.CharField(max_length=10)
    Numero_documento      = models.CharField(max_length=20)
    Correo_registrado     = models.CharField(max_length=255)
    P_nombre              = models.CharField(max_length=30)
    S_nombre              = models.CharField(max_length=30, blank=True, null=True)  # opcional
    P_apellido            = models.CharField(max_length=30)
    S_apellido            = models.CharField(max_length=30, blank=True, null=True)  # opcional
    Fecha_nacimiento      = models.DateField()
    Genero                = models.CharField(max_length=10)
    Celular               = models.CharField(max_length=20)
    Telefono_fijo         = models.CharField(max_length=30, blank=True, null=True)  # opcional
    Departamento          = models.CharField(max_length=50)
    Ciudad                = models.CharField(max_length=50)
    Direccion             = models.CharField(max_length=200)
    Residencia_fiscal     = models.CharField(max_length=10, blank=True, null=True)
    Residencia_fiscal_pais= models.CharField(max_length=100, blank=True, null=True)
    Patrimonio            = models.CharField(max_length=50)
    Declarante_renta      = models.CharField(max_length=5)
    PeP                   = models.CharField(max_length=5)
    Observaciones         = models.TextField(blank=True, null=True)               # opcional
    Numero_radicado       = models.CharField(max_length=20)
    Año                   = models.IntegerField()

    FUENTE_CHOICES = [
        ('salario', 'Salario'),
        ('otro',    'Otro'),
    ]
    Fuentes_recursos      = models.CharField(max_length=10, choices=FUENTE_CHOICES)
    Fuentes_recursos_otro = models.CharField(max_length=200, blank=True, null=True)
    Fecha_envio           = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Solicitud de Actualización"
        verbose_name_plural = "Solicitudes de Actualización"
        ordering            = ['-Fecha_envio']

    def __str__(self):
        return f"{self.P_nombre} {self.P_apellido} - {self.Numero_documento}"