from django.urls import path
from . import views

urlpatterns=[
    path('menuClases/', views.menuClases),
    
    path('menuClases/crearRecibo/', views.crearRecibo),
    
    path('menuClases/crearRecibo/guardarRecibo', views.guardarRecibo),
    
    path('menuClases/verRecibo', views.verRecibo),
    
    path('menuClases/crearClase', views.crearClase),
    
    path('menuClases/elegirProcedimiento', views.elegirProcedimiento),
    
    path('menuClases/crearClasePreferencia', views.crearClasePreferencia),
    
    path('menuClases/crearClasePreferencia-parte2/', views.crearClasePreferenciaParte2),
    
    path('menuClases/crearClasePreferencia-parte2/crearClasePreferencia-parte3/', views.crearClasePreferenciaParte3),
    
    path('menuClases/crearClase-parte2/', views.crearClaseParte2),
    
    path('menuClases/crearClase-parte2/crearClase-parte3/', views.crearClaseParte3),
    
    path('menuClases/verClases/', views.verClases),
    
    path('menuClases/verClases/editarClase/<id_clase>', views.editarClase),
    
    path('menuClases/verClases/editarClase/edicionClase/', views.edicionClase),
]