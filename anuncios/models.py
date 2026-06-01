from django.db import models
from django.utils import timezone


class AnuncioPequeno(models.Model):
    imagen       = models.ImageField(upload_to="anuncios/pequenos/", verbose_name="Imagen",
                                     help_text="Tamaño recomendado: 400×300 px")
    titulo       = models.CharField(max_length=100, blank=True, verbose_name="Título")
    subtitulo    = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo")
    enlace       = models.URLField(max_length=400, blank=True, verbose_name="Enlace")
    texto_boton  = models.CharField(max_length=60, default="Ver más", verbose_name="Texto del botón")
    activo       = models.BooleanField(default=True, verbose_name="Activo")
    orden        = models.PositiveIntegerField(default=0, verbose_name="Orden")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    fecha_fin    = models.DateField(null=True, blank=True, verbose_name="Fecha de fin")

    class Meta:
        ordering = ["orden"]
        verbose_name = "Anuncio pequeño"
        verbose_name_plural = "Anuncios pequeños"

    def __str__(self):
        return self.titulo or f"Anuncio pequeño #{self.pk}"

    def esta_vigente(self):
        hoy = timezone.now().date()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            return False
        if self.fecha_fin and self.fecha_fin < hoy:
            return False
        return True


class AnuncioGrande(models.Model):
    imagen       = models.ImageField(upload_to="anuncios/grandes/", verbose_name="Imagen",
                                     help_text="Tamaño recomendado: 800×600 px o más")
    enlace       = models.URLField(max_length=400, blank=True, verbose_name="Enlace (opcional)",
                                   help_text="Si lo llenas, la imagen será clickeable")
    activo       = models.BooleanField(default=True, verbose_name="Activo")
    orden        = models.PositiveIntegerField(default=0, verbose_name="Orden")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio")
    fecha_fin    = models.DateField(null=True, blank=True, verbose_name="Fecha de fin")

    class Meta:
        ordering = ["orden"]
        verbose_name = "Anuncio grande"
        verbose_name_plural = "Anuncios grandes"

    def __str__(self):
        return f"Anuncio grande #{self.pk}"

    def esta_vigente(self):
        hoy = timezone.now().date()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            return False
        if self.fecha_fin and self.fecha_fin < hoy:
            return False
        return True
    
class AnuncioFlotante(models.Model):
        imagen       = models.ImageField(upload_to='anuncios/flotantes/')
        enlace       = models.URLField(blank=True)
        activo       = models.BooleanField(default=True)
        orden        = models.PositiveIntegerField(default=0)
        fecha_inicio = models.DateField(null=True, blank=True)
        fecha_fin    = models.DateField(null=True, blank=True)

        class Meta:
            ordering = ['orden']
            verbose_name = 'Anuncio Flotante'
            verbose_name_plural = 'Anuncios Flotantes'

        def __str__(self):
            return f'Anuncio flotante #{self.pk}'