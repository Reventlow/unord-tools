# Generated by Django 3.2.3 on 2021-06-17 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_app', '0009_alter_one2oneinfo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=60)),
                ('user_report_it', models.CharField(max_length=30)),
                ('user_quicklink', models.URLField()),
                ('zendesk_link', models.URLField()),
                ('solved', models.BooleanField()),
                ('notes', models.TextField(max_length=448)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.asset')),
                ('case_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=60)),
                ('address_street', models.CharField(max_length=60)),
                ('address_postcode', models.CharField(max_length=30)),
                ('address_city', models.CharField(max_length=30)),
                ('company_telefon', models.CharField(max_length=30)),
                ('company_email', models.CharField(max_length=60)),
                ('company_support_telefon', models.CharField(max_length=30)),
                ('company_support_email', models.CharField(max_length=30)),
                ('notes', models.TextField(max_length=448)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('company_website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalServicePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=60)),
                ('notes', models.TextField(max_length=448)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeverityLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=60)),
                ('bootstrap_color', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalServiceContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=30)),
                ('cellphone', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.externalservice')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.externalserviceposition')),
            ],
        ),
        migrations.CreateModel(
            name='AssetLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_log', models.DateTimeField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('asset_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_app.assetcase')),
                ('log_written_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assetcase',
            name='external_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.externalservice'),
        ),
        migrations.AddField(
            model_name='assetcase',
            name='severity_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.severitylevel'),
        ),
    ]
