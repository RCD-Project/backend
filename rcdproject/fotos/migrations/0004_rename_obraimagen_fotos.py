# Generated by Django 5.1.6 on 2025-03-04 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fotos', '0003_obraimagen_delete_fotos'),
        ('obras', '0008_remove_obra_imagenes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ObraImagen',
            new_name='Fotos',
        ),
    ]
