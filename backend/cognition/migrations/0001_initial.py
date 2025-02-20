# Generated by Django 5.1.2 on 2025-02-20 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0026_alter_cognitionframe_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BallCandidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballcandidates', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='BallCandidatesTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballcandidatestop', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='BallModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballmodel', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='CameraMatrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameramatrix', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='CameraMatrixTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameramatrixtop', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='FieldPercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fieldpercept', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='FieldPerceptTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fieldpercepttop', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='GoalPercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goalpercept', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='GoalPerceptTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goalpercepttop', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='MultiBallPercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiballpercept', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='OdometryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='odometrydata', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='RansacCirclePercept2018',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ransaccirclepercept2018', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='RansacLinePercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ransaclinepercept', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='ScanLineEdgelPercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanlineedgelpercept', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='ScanLineEdgelPerceptTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanlineedgelpercepttop', to='api.cognitionframe')),
            ],
        ),
        migrations.CreateModel(
            name='ShortLinePercept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortlinepercept', to='api.cognitionframe')),
            ],
        ),
    ]
