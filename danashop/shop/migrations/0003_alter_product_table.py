# Generated by Django 5.2.1 on 2025-05-09 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_categorya_category'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='product',
            table='products',
        ),
    ]
