# Generated by Django 2.0.2 on 2019-12-09 12:23

from django.db import migrations
import rauwkost.models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0052_auto_20191209_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='button_link',
            field=rauwkost.models.VarCharField(blank=True, verbose_name='button link'),
        ),
        migrations.AddField(
            model_name='blog',
            name='button_text',
            field=rauwkost.models.VarCharField(blank=True, verbose_name='button text'),
        ),
    ]
