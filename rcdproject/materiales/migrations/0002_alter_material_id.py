# Generated by Django 5.1.5 on 2025-02-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
