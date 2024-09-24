# Generated by Django 5.0.6 on 2024-09-23 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_motionrepresentation_delete_sensorlog'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RobotData',
            new_name='Logs',
        ),
        migrations.AlterField(
            model_name='cognitionrepresentation',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cognition_repr', to='api.logs'),
        ),
        migrations.AlterField(
            model_name='image',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.logs'),
        ),
        migrations.AlterField(
            model_name='motionrepresentation',
            name='robotdata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motion_repr', to='api.logs'),
        ),
    ]