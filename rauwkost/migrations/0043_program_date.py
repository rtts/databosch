# Generated by Django 2.0.2 on 2019-11-22 12:55

from django.db import migrations, models
import rauwkost.models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0042_auto_20191122_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='date',
            field=models.DateField(default=rauwkost.models.default_date, verbose_name='datum'),
        ),
    ]
