# Generated by Django 2.0.2 on 2018-06-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0035_auto_20180603_0109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='sponsor',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='positie'),
            preserve_default=False,
        ),
    ]
