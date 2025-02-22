# Generated by Django 5.1.2 on 2025-02-22 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotionFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('frame_time', models.IntegerField(blank=True, null=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motionframe', to='common.log')),
            ],
            options={
                'verbose_name_plural': 'Motion Frames',
            },
        ),
        migrations.CreateModel(
            name='InertialSensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inertialsensordata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Inertial Sensor Data',
            },
        ),
        migrations.CreateModel(
            name='IMUData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imudata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'IMU Data',
            },
        ),
        migrations.CreateModel(
            name='GyrometerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gyrometerdata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Gyrometer Data',
            },
        ),
        migrations.CreateModel(
            name='FSRData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fsrdata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'FSR Data',
            },
        ),
        migrations.CreateModel(
            name='ButtonData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttondata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Button Data',
            },
        ),
        migrations.CreateModel(
            name='AccelerometerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accelerometerdata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Accelerometer Data',
            },
        ),
        migrations.CreateModel(
            name='MotionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motionstatus', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Motion Status',
            },
        ),
        migrations.CreateModel(
            name='MotorJointData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorjointdata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Motor Joint Data',
            },
        ),
        migrations.CreateModel(
            name='SensorJointData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensorjointdata', to='motion.motionframe')),
            ],
            options={
                'verbose_name_plural': 'Sensor Joint Data',
            },
        ),
        migrations.AddIndex(
            model_name='motionframe',
            index=models.Index(fields=['log', 'frame_number'], name='motion_moti_log_id_5ba14e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='motionframe',
            unique_together={('log', 'frame_number')},
        ),
    ]
