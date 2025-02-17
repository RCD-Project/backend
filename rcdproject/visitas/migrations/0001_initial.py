# Generated by Django 5.1.5 on 2025-02-17 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('obras', '0004_obra_imagenes'),
        ('tecnicos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Fecha de Visita')),
                ('motivo', models.CharField(max_length=200, verbose_name='Motivo')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitas', to='obras.obra', verbose_name='Obra')),
                ('tecnico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitas', to='tecnicos.tecnico', verbose_name='Técnico')),
            ],
        ),
    ]
