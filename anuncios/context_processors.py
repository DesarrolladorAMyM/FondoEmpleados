from django.utils import timezone
from .models import AnuncioPequeno, AnuncioGrande


def _vigentes(queryset):
    hoy = timezone.now().date()
    resultado = []
    for a in queryset:
        if a.fecha_inicio and a.fecha_inicio > hoy:
            continue
        if a.fecha_fin and a.fecha_fin < hoy:
            continue
        resultado.append(a)
    return resultado


def anuncio_popup(request):
    pequenos = _vigentes(AnuncioPequeno.objects.filter(activo=True).order_by("orden"))
    grandes  = _vigentes(AnuncioGrande.objects.filter(activo=True).order_by("orden"))

    return {
        "anuncios_popup":        pequenos,
        "anuncios_popup_grandes": grandes,
    }