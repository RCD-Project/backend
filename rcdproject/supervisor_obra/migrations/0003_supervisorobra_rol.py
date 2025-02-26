# Generated by Django 5.1.5 on 2025-02-25 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervisor_obra', '0002_supervisorobra_nivel_capacitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisorobra',
            name='rol',
            field=models.CharField(choices=[('super_administrador', 'Super Administrador'), ('coordinador_obra', 'Coordinador de Obra'), ('futuro_cliente', 'Futuro Cliente'), ('coordinador_retiro', 'Coordinador de Retiro'), ('supervisor_obra', 'Supervisor de Obra'), ('tecnico', 'Técnico'), ('cliente', 'Cliente')], default='supervisor_obra', max_length=50),
        ),
    ]
