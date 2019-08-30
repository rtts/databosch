# Generated by Django 2.0.2 on 2019-05-15 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('de_locatie', '0016_auto_20190507_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='begin',
            field=models.TimeField(blank=True, null=True, verbose_name='begintijd'),
        ),
        migrations.AddField(
            model_name='event',
            name='end',
            field=models.TimeField(blank=True, null=True, verbose_name='eindtijd'),
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Normaal'), (2, 'Video'), (4, 'Nieuws'), (5, 'Projecten'), (6, 'Partners'), (7, 'Foto'), (9, 'Agenda')], default=1, verbose_name='soort sectie'),
        ),
    ]