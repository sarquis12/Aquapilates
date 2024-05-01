from django.db import models

# Create your models here.

class Cliente(models.Model):
    dni = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=10)
    nacimiento = models.DateField()
    fecha_baja=models.DateField(null=True, default=None)
    def __str__(self):
        return f'{self.nombre} {self.apellido} '

class FichaMedica(models.Model):
    dni = models.OneToOneField(Cliente, on_delete=models.CASCADE, primary_key=True)
    celular_emergencia = models.CharField(max_length=8, null=True,default=None)
    altura = models.IntegerField(null=True, default=None)
    peso = models.IntegerField(null=True, default=None)
    obra_social = models.CharField(max_length=50,null=True, default=None)
    consideraciones = models.TextField(null=True,default=None)
    
    def __str__(self):
        return f'{self.celular_emergencia} {self.obra_social} '
    
    
