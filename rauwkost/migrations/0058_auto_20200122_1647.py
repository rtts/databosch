from django.db import migrations

def add_timeslots(apps, schema_editor):
    Program = apps.get_model('rauwkost', 'Program')
    ProgramTimeslot = apps.get_model('rauwkost', 'ProgramTimeslot')

    for p in Program.objects.all():
        if not ProgramTimeslot.objects.filter(program=p).exists():
            ProgramTimeslot(
                program = p,
                date = p.date,
                begin = p.begin,
                end = p.end,
            ).save()

class Migration(migrations.Migration):
    dependencies = [
        ('rauwkost', '0057_programtimeslot'),
    ]

    operations = [
        migrations.RunPython(add_timeslots, migrations.RunPython.noop),
    ]
