# Generated by Django 3.1.2 on 2020-12-17 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_productpurchase_productpurchasemanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductPurchaseManager',
        ),
    ]
