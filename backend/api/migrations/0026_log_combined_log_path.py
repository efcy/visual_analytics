# Generated by Django 5.0.6 on 2024-10-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_image_blurredness_value_image_brightness_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='combined_log_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]