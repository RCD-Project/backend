# Generated by Django 5.1.6 on 2025-03-07 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntolimpio', '0010_remove_puntoacopio_clasificacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntolimpio',
            name='cantidad',
            field=models.IntegerField(default=0, null=True, verbose_name='Cantidad'),
        ),
    ]
