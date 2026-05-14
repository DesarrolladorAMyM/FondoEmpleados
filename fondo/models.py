from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.

def validar_imagen_banner(imagen):
    img = Image.open(imagen)
    ancho, alto = img.size

    if ancho < 1774:
        raise ValidationError(
            f"La imagen es muy angosta ({ancho}px). Mínimo 1774px de ancho."
        )
    if alto < 887:
        raise ValidationError(
            f"La imagen es muy baja ({alto}px). Mínimo 887px de alto."
        )
    proporcion = ancho / alto
    if not (1.9 <= proporcion <= 2.1):   # margen ±5% alrededor del 2:1
        raise ValidationError(
            f"La proporción ({ancho}x{alto}) no es adecuada. "
            f"Usa imágenes de 1774x887px (relación 2:1)."
        )
        
class Banner(models.Model):
    titulo = models.CharField(
        max_length=100,
        help_text="Nombre interno para identificar el banner (no aparece en el sitio)"
    )
    imagen = models.ImageField(
        upload_to='banners/',
        validators=[validar_imagen_banner],
        help_text="Imagen horizontal recomendada: 1774x887px. Formatos: JPG, PNG, WEBP"
    )
    activo = models.BooleanField(default=True, help_text="Desactiva para ocultar sin borrar")
    orden = models.PositiveIntegerField(default=0, help_text="Menor número = aparece primero")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['orden']

    def __str__(self):
        return self.titulo
        
        
class MensajeContacto(models.Model):
    Nombre=models.CharField(max_length=100)
    Empresa=models.CharField(max_length=100)
    Correo=models.EmailField()
    Telefono=models.CharField(max_length=20)
    Servicio=models.CharField(max_length=50)
    Mensaje=models.TextField()
    Fecha_envio=models.DateTimeField(auto_now_add=True)   #auto_now_add esto hace que traiga la hora y fecha actual
    
    class Meta:
        verbose_name="Contacto"
        verbose_name_plural="Contactos"
        
    def __str__(self):
        return f"{self.Nombre} - {self.Correo}"
    