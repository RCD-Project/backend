# Generated by Django 5.1.6 on 2025-03-04 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fotos', '0001_initial'),
        ('obras', '0008_remove_obra_imagenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fotos',
            name='tipo_imagen',
        ),
        migrations.RemoveField(
            model_name='fotos',
            name='ubicacion_server',
        ),
        migrations.RemoveField(
            model_name='fotos',
            name='visita',
        ),
        migrations.AddField(
            model_name='fotos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='obras/imagenes/'),
        ),
        migrations.AddField(
            model_name='fotos',
            name='obra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagenes_set', to='obras.obra'),
        ),
        migrations.AlterField(
            model_name='fotos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
