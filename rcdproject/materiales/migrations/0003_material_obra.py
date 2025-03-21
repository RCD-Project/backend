# Generated by Django 5.1.5 on 2025-02-19 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0002_alter_material_id'),
        ('obras', '0006_remove_obra_localidad_barrio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='obra',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='materiales', to='obras.obra', verbose_name='Obra'),
            preserve_default=False,
        ),
    ]
