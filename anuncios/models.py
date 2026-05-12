from django.db import models
from django.utils import timezone

class Anuncio(models.Model):
    imagen      = models.ImageField(upload_to="anuncios/", verbose_name="Imagen",
                                    help_text="Tamaño recomendado: 400×300 px")
    titulo      = models.CharField(max_length=100, blank=True, verbose_name="Título")
    subtitulo   = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo")
    enlace      = models.URLField(max_length=400, blank=True, verbose_name="Enlace",
                                  help_text="URL a donde va al hacer clic en la imagen o 'Ver más'")
    texto_boton = models.CharField(max_length=60, default="Ver más",
                                   verbose_name="Texto del botón")
    activo      = models.BooleanField(default=True, verbose_name="Activo")
    orden       = models.PositiveIntegerField(default=0, verbose_name="Orden")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    fecha_fin    = models.DateField(null=True, blank=True, verbose_name="Fecha de fin")

    class Meta:
        ordering = ["orden"]
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"

    def __str__(self):
        return self.titulo or f"Anuncio #{self.pk}"

    def esta_vigente(self):
        hoy = timezone.now().date()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            return False
        if self.fecha_fin and self.fecha_fin < hoy:
            return False
        return True