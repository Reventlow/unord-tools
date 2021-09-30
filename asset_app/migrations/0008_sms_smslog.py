# Generated by Django 3.2.3 on 2021-09-27 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0007_auto_20210913_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('automatic', models.BooleanField(default=False)),
                ('manual', models.BooleanField(default=False)),
                ('button_name', models.CharField(max_length=30)),
                ('button_level', models.IntegerField(blank=True, null=True)),
                ('sms_message', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='SmsLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_name', models.CharField(max_length=60)),
                ('sms_number', models.CharField(max_length=8)),
                ('sms_timestamp', models.DateTimeField()),
                ('sms_msg_sent', models.CharField(max_length=400)),
                ('sms_msg_type', models.CharField(max_length=20)),
                ('loan_asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.loan_asset')),
                ('sms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.sms')),
            ],
        ),
    ]
