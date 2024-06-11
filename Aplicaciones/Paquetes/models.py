from django.db import models

# Create your models here.

class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    cant_clas_sem = models.IntegerField()
    precio_paquete = models.IntegerField()
    fechaCaducidad_paquete = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return f'Paquete {self.id_paquete} - Clases: {self.cant_clas_sem} - Precio: {self.precio_paquete}'