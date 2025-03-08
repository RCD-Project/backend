# Generated by Django 5.1.6 on 2025-03-08 14:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('obras', '0011_remove_obra_archivo_archivoobra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mezclado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pesaje', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Pesaje')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mezclados', to='obras.obra')),
            ],
        ),
        migrations.CreateModel(
            name='MezcladoImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='mezclados/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])], verbose_name='Imagen')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Subida')),
                ('mezclado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='mezclados.mezclado')),
            ],
        ),
    ]
