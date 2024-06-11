from django.urls import path
from . import views

urlpatterns = [
    path('Turnos/', views.turnos),
    path('TurnosDisponibles/', views.turnosDisponibles),
    path('registrarTurno/',views.registrarTurno),
    path('Turnos/eliminarTurno/<id_turno>',views.eliminarTurno),
    path('Turnos/activarTurno/<id_turno>',views.activarTurno),
    
    
]