# Generated by Django 5.1.2 on 2024-10-25 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_image_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xabslsymbolcomplete',
            name='id',
        ),
        migrations.AlterField(
            model_name='xabslsymbolcomplete',
            name='log_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='xabsl_symbols3', serialize=False, to='api.log'),
        ),
    ]