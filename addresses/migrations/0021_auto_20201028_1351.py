# Generated by Django 3.1.2 on 2020-10-28 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0020_auto_20201028_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=120),
        ),
    ]
