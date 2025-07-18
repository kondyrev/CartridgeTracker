# Generated by Django 5.2.3 on 2025-06-24 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartridges', '0004_alter_cartridgeinventory_cartridge_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrival',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='CartridgeMinStockGlobal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_stock', models.PositiveIntegerField(verbose_name='Минимальный остаток')),
                ('cartridge', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='minstock', to='cartridges.cartridge')),
            ],
        ),
        migrations.DeleteModel(
            name='CartridgeMinStock',
        ),
    ]
