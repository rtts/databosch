# Generated by Django 2.0.2 on 2019-11-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0043_program_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='active',
            field=models.BooleanField(default=False, verbose_name='actief'),
        ),
    ]