from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('registrarCliente/',views.registrarCliente),
    path('eliminacionCliente/<dni>',views.eliminacionCliente),
    path('edicionCliente/<dni>',views.edicionCliente),
    path('editarCliente/',views.editarCliente),
    path('verFichaMedica/<dni>', views.verFichaMedica),
    path('editarFichaMedica/',views.editarFichaMedica),
    path('activarCliente/<dni>', views.activarCliente),
    path('accounts/logout/', views.salir),
]
