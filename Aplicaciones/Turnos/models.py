from django.db import models

# Create your models here.

class Turnos(models.Model):
    id_turno = models.AutoField(primary_key=True)
    dia_turno = models.CharField(max_length=15, verbose_name='día de la semana')
    rango_turno = models.CharField(max_length=15, verbose_name='rango de horario de la clase')
    cant_maxima = models.IntegerField(verbose_name='cupo máximo de alumnos por turno')
    fecha_baja=models.DateField(null=True, default=None)
    
    def __str__(self):
        return f"{self.dia_turno} - {self.rango_turno}"

