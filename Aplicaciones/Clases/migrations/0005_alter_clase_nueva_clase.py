# Generated by Django 5.0.3 on 2024-03-26 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clases', '0004_clase_nueva_clase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clase',
            name='nueva_clase',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Clases.clase'),
        ),
    ]
