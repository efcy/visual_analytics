# Generated by Django 5.0.6 on 2024-08-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vatuser',
            name='name',
        ),
        migrations.AlterField(
            model_name='vatuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='vatuser',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]