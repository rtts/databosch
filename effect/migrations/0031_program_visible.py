# Generated by Django 2.0.2 on 2018-03-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0030_auto_20180322_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='actief'),
        ),
    ]
