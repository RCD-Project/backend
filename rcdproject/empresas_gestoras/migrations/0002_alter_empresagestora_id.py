# Generated by Django 5.1.5 on 2025-02-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas_gestoras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresagestora',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
