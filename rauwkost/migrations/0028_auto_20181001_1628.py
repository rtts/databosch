# Generated by Django 2.0.2 on 2018-10-01 14:28

from django.db import migrations, models
import rauwkost.models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0027_auto_20181001_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='datum')),
                ('header', models.FileField(blank=True, upload_to='', verbose_name='header')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.AlterField(
            model_name='config',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(1, 'Programmajaar'), (10, 'Footer midden'), (11, 'Footer links'), (12, 'Footer rechts'), (20, 'Homepage header'), (25, 'Extra menu items'), (30, 'Extra CSS')], unique=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='year',
            field=models.PositiveIntegerField(default='2018', verbose_name='programmajaar'),
        ),
    ]