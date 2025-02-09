# Generated by Django 5.1.2 on 2024-10-18 20:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='framefilter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame_filter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='api.event'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Annotation', to='api.image'),
        ),
        migrations.AddField(
            model_name='log',
            name='game_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robot_data', to='api.game'),
        ),
        migrations.AddField(
            model_name='image',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.log'),
        ),
        migrations.AddField(
            model_name='framefilter',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame_filter', to='api.log'),
        ),
        migrations.AddField(
            model_name='cognitionrepresentation',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cognition_repr', to='api.log'),
        ),
        migrations.AddField(
            model_name='behavioroptionstate',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='behavior_options_states', to='api.log'),
        ),
        migrations.AddField(
            model_name='behavioroption',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='behavior_options', to='api.log'),
        ),
        migrations.AddField(
            model_name='behaviorframeoption',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='behavior_frame_option', to='api.log'),
        ),
        migrations.AddField(
            model_name='logstatus',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_status', to='api.log'),
        ),
        migrations.AddField(
            model_name='motionrepresentation',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motion_repr', to='api.log'),
        ),
        migrations.AddField(
            model_name='xabslsymbolcomplete',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xabsl_symbols3', to='api.log', unique=True),
        ),
        migrations.AddField(
            model_name='xabslsymbolsparse',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xabsl_symbol_sparse', to='api.log'),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('event_id', 'start_time', 'half')},
        ),
        migrations.AddIndex(
            model_name='cognitionrepresentation',
            index=models.Index(fields=['log_id', 'frame_number'], name='api_cogniti_log_id__623c00_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='cognitionrepresentation',
            unique_together={('log_id', 'frame_number', 'representation_name')},
        ),
        migrations.AddIndex(
            model_name='behaviorframeoption',
            index=models.Index(fields=['log_id', 'frame', 'options_id'], name='api_behavio_log_id__008378_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='behaviorframeoption',
            unique_together={('log_id', 'options_id', 'frame', 'active_state')},
        ),
        migrations.AddIndex(
            model_name='xabslsymbolcomplete',
            index=models.Index(fields=['log_id'], name='api_xabslsy_log_id__b1b0d0_idx'),
        ),
        migrations.AddIndex(
            model_name='xabslsymbolsparse',
            index=models.Index(fields=['log_id', 'frame'], name='api_xabslsy_log_id__605083_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='xabslsymbolsparse',
            unique_together={('log_id', 'frame')},
        ),
    ]
