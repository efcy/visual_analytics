# Generated by Django 5.0.6 on 2024-10-04 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_xabslsymbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='XabslSymbol2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.IntegerField(blank=True, null=True)),
                ('output_decimal', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='xabslsymbol',
            unique_together={('log_id', 'frame', 'symbol_type', 'symbol_name')},
        ),
        migrations.AddIndex(
            model_name='xabslsymbol',
            index=models.Index(fields=['log_id', 'frame'], name='api_xabslsy_log_id__633ce7_idx'),
        ),
        migrations.AddField(
            model_name='xabslsymbol2',
            name='log_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xabsl_symbols2', to='api.log'),
        ),
        migrations.AddIndex(
            model_name='xabslsymbol2',
            index=models.Index(fields=['log_id', 'frame'], name='api_xabslsy_log_id__036a0b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='xabslsymbol2',
            unique_together={('log_id', 'frame')},
        ),
    ]
