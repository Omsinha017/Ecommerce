# Generated by Django 3.1 on 2020-10-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0006_auto_20201003_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=120),
        ),
    ]
