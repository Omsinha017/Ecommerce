# Generated by Django 3.1.2 on 2020-12-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200823_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_digital',
            field=models.BooleanField(default=False),
        ),
    ]
