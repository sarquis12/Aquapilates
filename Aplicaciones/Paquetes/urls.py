from django.urls import path
from . import views

urlpatterns = [
    path('Paquetes/', views.Paquetes),
    path('registrarPaquete/',views.registrarPaquete),
    path('Paquetes/eliminarPaquete/<id_paquete>',views.eliminarPaquete),
    path('Paquetes/activarPaquete/<id_paquete>',views.activarPaquete),
    
]