# Generated by Django 2.0.2 on 2018-06-02 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0036_auto_20180603_0134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ['position'], 'verbose_name': 'Fonds', 'verbose_name_plural': 'Fondsen'},
        ),
        migrations.AddField(
            model_name='partner',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='positie'),
            preserve_default=False,
        ),
    ]