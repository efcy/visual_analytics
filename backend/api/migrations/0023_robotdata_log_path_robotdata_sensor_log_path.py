# Generated by Django 5.0.6 on 2024-08-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_robotdata_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='robotdata',
            name='log_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='robotdata',
            name='sensor_log_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]