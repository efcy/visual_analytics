# Generated by Django 5.1.2 on 2024-11-11 15:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_logstatus_multiballpercept'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='annotation_id',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='id',
        ),
        migrations.AddField(
            model_name='annotation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annotation',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='Annotation', serialize=False, to='api.image'),
        ),
    ]
