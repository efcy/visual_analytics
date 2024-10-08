# Generated by Django 5.0.6 on 2024-09-23 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_robotdata_representations_log_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CognitionRepresentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('data', models.JSONField(blank=True, null=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cognition_repr', to='api.robotdata')),
            ],
            options={
                'unique_together': {('log', 'frame_number', 'name')},
            },
        ),
        migrations.DeleteModel(
            name='Representations',
        ),
    ]
