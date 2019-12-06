# Generated by Django 2.0.2 on 2019-12-04 10:46

from django.db import migrations, models
import rauwkost.models


class Migration(migrations.Migration):

    dependencies = [
        ('rauwkost', '0047_remove_sublocation_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', rauwkost.models.VarCharField()),
                ('icon', models.ImageField(upload_to='')),
                ('hyperlink', models.URLField()),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]