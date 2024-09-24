# Generated by Django 5.0.6 on 2024-09-23 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_representations_robotdata_representation_list_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='representations',
            old_name='robotdata',
            new_name='log',
        ),
        migrations.AlterUniqueTogether(
            name='representations',
            unique_together={('log', 'frame_number', 'name')},
        ),
    ]