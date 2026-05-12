from django.utils import timezone
from .models import Anuncio

def anuncio_popup(request):
    hoy = timezone.now().date()
    anuncios = []

    for a in Anuncio.objects.filter(activo=True).order_by("orden"):
        if a.fecha_inicio and a.fecha_inicio > hoy:
            continue
        if a.fecha_fin and a.fecha_fin < hoy:
            continue
        anuncios.append(a)

    return {"anuncios_popup": anuncios}