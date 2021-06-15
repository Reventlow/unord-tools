# Generated by Django 3.2.3 on 2021-06-15 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_app', '0007_routinelog_routines'),
    ]

    operations = [
        migrations.CreateModel(
            name='One2OneInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('completed', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, default='', max_length=448, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['completed', 'name'],
            },
        ),
        migrations.CreateModel(
            name='One2OneInfoLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('notes', models.TextField(blank=True, default='', max_length=448, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.locations')),
                ('one_2_one_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.one2oneinfo')),
            ],
            options={
                'ordering': ['location', 'name'],
            },
        ),
    ]
