from django.db import models

# Create your models here.
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
    