from django.db import migrations

def set_is_experiment_false(apps, schema_editor):
    Log = apps.get_model('api', 'Log')
    Log.objects.all().update(is_experiment=False)

def reverse_migration(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0012_log_is_experiment'), 
    ]

    operations = [
        migrations.RunPython(set_is_experiment_false, reverse_migration),
    ]