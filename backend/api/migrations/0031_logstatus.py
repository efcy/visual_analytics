# Generated by Django 5.0.6 on 2024-10-07 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_alter_xabslsymbol_symbol_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BallModel', models.IntegerField(blank=True, null=True)),
                ('CameraMatrix', models.IntegerField(blank=True, null=True)),
                ('CameraMatrixTop', models.IntegerField(blank=True, null=True)),
                ('FieldPercept', models.IntegerField(blank=True, null=True)),
                ('FieldPerceptTop', models.IntegerField(blank=True, null=True)),
                ('GoalPercept', models.IntegerField(blank=True, null=True)),
                ('GoalPerceptTop', models.IntegerField(blank=True, null=True)),
                ('RansacLinePercept', models.IntegerField(blank=True, null=True)),
                ('RansacCirclePercept2018', models.IntegerField(blank=True, null=True)),
                ('ShortLinePercept', models.IntegerField(blank=True, null=True)),
                ('ScanLineEdgelPercept', models.IntegerField(blank=True, null=True)),
                ('ScanLineEdgelPerceptTop', models.IntegerField(blank=True, null=True)),
                ('OdometryData', models.IntegerField(blank=True, null=True)),
                ('num_cognition_frames', models.IntegerField(blank=True, null=True)),
                ('num_motion_frames', models.IntegerField(blank=True, null=True)),
                ('num_jpg_bottom', models.IntegerField(blank=True, null=True)),
                ('num_jpg_top', models.IntegerField(blank=True, null=True)),
                ('num_bottom', models.IntegerField(blank=True, null=True)),
                ('num_top', models.IntegerField(blank=True, null=True)),
                ('log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_status', to='api.log')),
            ],
        ),
    ]