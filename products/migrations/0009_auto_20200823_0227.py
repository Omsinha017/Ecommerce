# Generated by Django 3.0.3 on 2020-08-22 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
