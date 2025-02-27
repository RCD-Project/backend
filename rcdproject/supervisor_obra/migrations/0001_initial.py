# Generated by Django 5.1.5 on 2025-02-10 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('obras', '0002_solicitudobra'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorObra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('obra', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to='obras.obra')),
            ],
        ),
    ]
