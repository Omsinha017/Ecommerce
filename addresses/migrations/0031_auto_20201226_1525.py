# Generated by Django 3.1.2 on 2020-12-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0030_auto_20201226_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], max_length=120),
        ),
    ]
