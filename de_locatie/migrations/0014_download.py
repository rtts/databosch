# Generated by Django 2.0.2 on 2019-02-28 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('de_locatie', '0013_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='bestand')),
            ],
            options={
                'ordering': ['file'],
            },
        ),
    ]