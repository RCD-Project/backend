# Generated by Django 5.1.6 on 2025-03-03 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formularios', '0004_formularios_otras_observaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='formularios',
            name='acciones_tomadas',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Acciones tomadas'),
        ),
    ]
