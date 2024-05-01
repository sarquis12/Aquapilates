# Generated by Django 5.0.3 on 2024-03-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_turnos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id_paquete', models.AutoField(primary_key=True, serialize=False)),
                ('cant_clas_sem', models.IntegerField(verbose_name='cantidad de clases por semana')),
                ('precio_paquete', models.IntegerField(verbose_name='precio del paquete')),
                ('fechaCaducidad_paquete', models.DateField(blank=True, default=None, null=True, verbose_name='fecha en la que el paquete dejo de venderse')),
            ],
        ),
    ]
