# Generated by Django 5.1.5 on 2025-02-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacitacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacitacion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
