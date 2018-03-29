# Generated by Django 2.0.2 on 2018-03-29 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('effect', '0031_program_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='high-res origineel')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='effect.Program')),
            ],
            options={
                'verbose_name': 'foto',
                'verbose_name_plural': 'foto’s',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProgramVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='high-res origineel')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='effect.Program')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'video’s',
                'ordering': ['position'],
            },
        ),
    ]
