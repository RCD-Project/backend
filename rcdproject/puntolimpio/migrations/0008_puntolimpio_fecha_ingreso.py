# Generated by Django 5.1.6 on 2025-03-03 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntolimpio', '0007_puntoacopio'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntolimpio',
            name='fecha_ingreso',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Ingreso'),
        ),
    ]
