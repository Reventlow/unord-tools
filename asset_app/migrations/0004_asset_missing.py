# Generated by Django 3.2.3 on 2021-08-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0003_auto_20210705_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='missing',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
