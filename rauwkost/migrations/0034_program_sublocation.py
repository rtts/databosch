# Generated by Django 2.0.2 on 2018-12-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0033_auto_20181003_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='sublocation',
            field=models.CharField(blank=True, max_length=255, verbose_name='plek'),
        ),
    ]