# Generated by Django 3.1.2 on 2020-12-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0025_auto_20201217_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('shipping', 'Shipping'), ('billing', 'Billing')], max_length=120),
        ),
    ]
