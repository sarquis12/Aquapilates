from django.db import models
from Aplicaciones.Turnos.models import Turnos
from Aplicaciones.Paquetes.models import Paquete
from Aplicaciones.clientes.models import Cliente
# Create your models here.

class Recibo(models.Model):
    id_recibo = models.AutoField(primary_key=True)
    dni = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, default=None)
    fecha_recibo = models.DateField()
    importe = models.IntegerField()
    métodoDePago = models.CharField(max_length=50)
    usado = models.DateField(null=True, default=None)

    class Meta:
        verbose_name_plural = "Recibos"
        verbose_name = "Recibo"
        db_table = "recibos"

    def __str__(self):
        return f"Recibo #{self.id_recibo} - DNI: {self.dni} - importe: {self.importe}"
    




class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    DNI = models.CharField(max_length=10)
    id_paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, null=True, default=None)
    id_recibo = models.ForeignKey(Recibo, on_delete=models.CASCADE, null=True, default=None)
    fecha_reserva= models.DateField()

    class Meta:
        verbose_name_plural = "Reservas"
        verbose_name = "Reserva"
        db_table = "reservas"

    def __str__(self):
        return f"Reserva #{self.id_reserva} - DNI: {self.DNI} - Fecha de la reserva: {self.fecha_reserva}"
    
class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    id_turno = models.ForeignKey(Turnos,on_delete=models.CASCADE)
    id_reserva = models.ForeignKey(Reserva,on_delete=models.CASCADE)
    fecha_clase = models.DateField()
    asistencia = models.BooleanField(null=True, default=None)
    observaciones = models.TextField(default=None, null=True)
    preparacion = models.TextField(default=None, null=True)
    nueva_clase= models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    fecha_cancelado = models.DateField(null=True, default=None)
    
    Force = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Clases"
        verbose_name = "Clase"
        db_table = "clase"

    def __str__(self):
        return f"Clase #{self.id_clase} - Fecha: {self.fecha_clase}"   