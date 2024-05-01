# Generated by Django 5.0.2 on 2024-03-10 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id_turno', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('dia_turno', models.CharField(max_length=15, verbose_name='día de la semana')),
                ('rango_turno', models.CharField(max_length=15, verbose_name='rango de horario de la clase')),
                ('cant_maxima', models.IntegerField(verbose_name='cupo máximo de alumnos por turno')),
            ],
        ),
    ]