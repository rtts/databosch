# Generated by Django 2.0.2 on 2018-10-03 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maakdenbosch', '0061_auto_20171120_1630'),
        ('rauwkost', '0030_auto_20181001_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='maakdenbosch.Entiteit')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='rauwkost.Program')),
            ],
            options={
                'verbose_name': 'partner',
                'verbose_name_plural': 'partners',
            },
        ),
        migrations.AlterModelOptions(
            name='newsitem',
            options={'ordering': ['-date'], 'verbose_name': 'nieuwsbericht', 'verbose_name_plural': 'nieuwsberichten'},
        ),
        migrations.AlterField(
            model_name='config',
            name='parameter',
            field=models.PositiveIntegerField(choices=[(10, 'Footer midden'), (11, 'Footer links'), (12, 'Footer rechts'), (25, 'Extra menu items'), (30, 'Extra CSS')], unique=True),
        ),
    ]
