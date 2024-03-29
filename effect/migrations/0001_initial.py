# Generated by Django 3.1.1 on 2020-09-23 14:32

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maakdenbosch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.PositiveIntegerField(choices=[(1, 'Footer tekst')])),
                ('content', models.TextField(verbose_name='inhoud')),
            ],
            options={
                'verbose_name': 'Parameter',
                'ordering': ['parameter'],
            },
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='afbeelding')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='afbeelding')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
                ('visible', models.BooleanField(default=True, verbose_name='actief')),
            ],
            options={
                'verbose_name': 'Locatie',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL')),
                ('menu', models.BooleanField(default=True, verbose_name='zichtbaar in het menu')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='effect.header')),
                ('mobile_header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='effect.header')),
            ],
            options={
                'verbose_name': 'Pagina',
                'verbose_name_plural': 'Pagina’s',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
                ('logo', models.ImageField(upload_to='')),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Fonds',
                'verbose_name_plural': 'Fondsen',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='actief')),
                ('visible_in_timetable', models.BooleanField(blank=True, verbose_name='zichtbaar in blokkenschema')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='afbeelding')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='beschrijving')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='effect.location', verbose_name='locatie')),
            ],
            options={
                'verbose_name': 'Programmaonderdeel',
                'verbose_name_plural': 'Programmaonderdelen',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('subtitle', models.CharField(blank=True, max_length=255, verbose_name='onndertitel')),
                ('slug', models.SlugField()),
                ('active', models.BooleanField(default=True, verbose_name='actief')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='foto')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
                ('entity', models.ForeignKey(blank=True, help_text='Kies hier de DataBosch entiteit die dit project vertegenwoordigt', null=True, on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.entiteit', verbose_name='bestaande entiteit')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='maakdenbosch.persoon', verbose_name='projectleider')),
            ],
            options={
                'verbose_name_plural': 'Projecten',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('name', models.CharField(max_length=255, verbose_name='Naam')),
                ('image', models.ImageField(upload_to='', verbose_name='afbeelding')),
                ('hyperlink', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Social Media',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
                ('logo', models.ImageField(upload_to='')),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='naam')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateTimeField(default=datetime.datetime(2018, 6, 9, 12, 0), verbose_name='begintijd')),
                ('end', models.DateTimeField(default=datetime.datetime(2018, 6, 9, 12, 0), verbose_name='eindtijd')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to='effect.program')),
            ],
            options={
                'ordering': ['begin'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('visibility', models.PositiveIntegerField(choices=[(1, 'Altijd zichtbaar'), (2, 'Alleen op desktop'), (3, 'Onzichtbaar')], default=1, verbose_name='zichtbaarheid')),
                ('type', models.PositiveIntegerField(choices=[(1, 'Normaal'), (2, 'Video'), (4, 'Nieuws'), (5, 'Projecten'), (6, 'Partners'), (7, 'Foto'), (8, 'Formulier'), (9, 'Programma'), (10, 'Timetable')], default=1, verbose_name='soort sectie')),
                ('show_partners', models.BooleanField(default=False, verbose_name='laat fondsen zien in partnersectie')),
                ('show_sponsors', models.BooleanField(default=False, verbose_name='laat sponsors zien in partnersectie')),
                ('show_partnerships', models.BooleanField(default=False, verbose_name='laat alle projectpartners zien in partnersectie')),
                ('color', models.PositiveIntegerField(choices=[(1, 'Wit'), (2, 'Oranje'), (3, 'Groen')], default=1, verbose_name='kleur')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='titel')),
                ('contents', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='afbeelding')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')),
                ('button', models.CharField(blank=True, max_length=255, verbose_name='button')),
                ('hyperlink', models.CharField(blank=True, max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='effect.icon')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='effect.page', verbose_name='pagina')),
            ],
            options={
                'verbose_name': 'sectie',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProjectPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='high-res origineel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='effect.project')),
            ],
            options={
                'verbose_name': 'Foto',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='effect.Tag'),
        ),
        migrations.CreateModel(
            name='ProgramVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Plak hier een YouTube, Vimeo, of SoundCloud link')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='effect.program')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'video’s',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProgramPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('image', models.ImageField(upload_to='', verbose_name='high-res origineel')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='effect.program')),
            ],
            options={
                'verbose_name': 'foto',
                'verbose_name_plural': 'foto’s',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProgramHyperlink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hyperlinks', to='effect.program')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.linktype')),
            ],
            options={
                'verbose_name': 'social media link',
            },
        ),
        migrations.AddField(
            model_name='program',
            name='tags',
            field=models.ManyToManyField(blank=True, to='effect.Tag'),
        ),
        migrations.CreateModel(
            name='Partnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='positie')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maakdenbosch.entiteit')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partnerships', to='effect.project')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='datum')),
                ('title', models.CharField(max_length=255, verbose_name='titel')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='foto')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='inhoud')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='effect.project')),
            ],
            options={
                'verbose_name': 'Nieuwsbericht',
                'verbose_name_plural': 'Nieuwsberichten',
                'ordering': ['-date'],
            },
        ),
    ]
