# Generated by Django 3.1 on 2020-10-10 08:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='card',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
