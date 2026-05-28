from django.urls import path 
from . import views 

from django.conf import settings
from django.conf.urls.static import static

# rutas 

urlpatterns=[
    path('FondoEmpleados/PortalAsociados/', views.Asociados, name="PortalAsociados"),
    path('FondoEmpleados/verificar-paso1/', views.verificar_paso1, name='verificar_paso1'),
]