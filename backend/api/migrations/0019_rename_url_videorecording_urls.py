# Generated by Django 5.1.2 on 2025-02-15 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_videorecording'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videorecording',
            old_name='url',
            new_name='urls',
        ),
    ]
