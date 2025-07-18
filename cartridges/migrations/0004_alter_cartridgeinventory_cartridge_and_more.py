# Generated by Django 5.2.3 on 2025-06-24 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartridges', '0003_remove_cartridge_current_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridgeinventory',
            name='cartridge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='cartridges.cartridge'),
        ),
        migrations.AlterField(
            model_name='cartridgeminstock',
            name='cartridge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minstock_set', to='cartridges.cartridge'),
        ),
    ]
