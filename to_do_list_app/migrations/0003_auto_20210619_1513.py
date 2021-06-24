# Generated by Django 3.2.3 on 2021-06-19 13:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_list_app', '0002_jobs_to_do_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobs',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]