# Generated by Django 3.1 on 2020-10-19 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0017_auto_20201020_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('shipping', 'Shipping'), ('billing', 'Billing')], max_length=120),
        ),
    ]
