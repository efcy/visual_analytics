# Generated by Django 5.0.6 on 2024-09-29 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_behavioroption_behavioroptionstate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='behavioroptionstate',
            old_name='options_id',
            new_name='option_id',
        ),
    ]
