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
            name='BehaviorFrameOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xabsl_internal_option_id', models.IntegerField(blank=True, null=True)),
                ('option_name', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorOptionState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xabsl_internal_state_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('target', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='XabslSymbolComplete',
            fields=[
                ('log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='xabsl_symbol_complete', serialize=False, to='common.log')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'XabslSymbolComplete',
            },
        ),
        migrations.CreateModel(
            name='XabslSymbolSparse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'XabslSymbolSparse',
            },
        ),
    ]
