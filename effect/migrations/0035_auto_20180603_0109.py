# Generated by Django 2.0.2 on 2018-06-02 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0034_auto_20180524_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeslot',
            options={'ordering': ['begin']},
        ),
        migrations.AlterField(
            model_name='program',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Normaal'), (2, 'Video'), (4, 'Nieuws'), (5, 'Projecten'), (6, 'Partners'), (7, 'Foto'), (8, 'Formulier'), (9, 'Programma'), (10, 'Timetable')], default=1, verbose_name='soort sectie'),
        ),
    ]
