# Generated by Django 5.1.2 on 2024-11-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_logstatus_ballcandidates_logstatus_ballcandidatestop'),
    ]

    operations = [
        migrations.AddField(
            model_name='logstatus',
            name='MultiBallPercept',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
