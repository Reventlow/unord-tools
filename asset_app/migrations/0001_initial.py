# Generated by Django 3.2.3 on 2021-05-21 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('mac_address', models.CharField(blank=True, max_length=30, null=True)),
                ('serial', models.CharField(blank=True, default=None, max_length=30, null=True, unique=True)),
                ('purchased_date', models.DateField(blank=True, null=True)),
                ('may_be_loaned', models.BooleanField(blank=True, default=False, null=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('ip', models.CharField(blank=True, max_length=90, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asset_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Loaner_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_inspected', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('image_date', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/images')),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_requests_created', to='asset_app.locations')),
                ('room_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_requests_created', to='asset_app.room_type')),
            ],
            options={
                'ordering': ['location', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('asset_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.asset_type')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Loan_asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loaner_address', models.TextField(blank=True, max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('loaner_name', models.CharField(max_length=60)),
                ('loaner_quicklink', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('loaner_telephone_number', models.CharField(max_length=30)),
                ('loaner_email', models.EmailField(max_length=254)),
                ('loan_date', models.DateField()),
                ('return_date', models.DateField()),
                ('returned', models.BooleanField(blank=True, default=False, null=True)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.asset')),
            ],
        ),
        migrations.CreateModel(
            name='Bundle_reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loaner_name', models.CharField(max_length=60)),
                ('loaner_email', models.EmailField(max_length=254)),
                ('loaner_telephone_number', models.CharField(max_length=30)),
                ('loaner_quicklink', models.URLField(blank=True, null=True)),
                ('amount', models.IntegerField()),
                ('series', models.CharField(blank=True, max_length=60, null=True)),
                ('course_name', models.CharField(blank=True, max_length=30, null=True)),
                ('loan_date', models.DateField()),
                ('return_date', models.DateField()),
                ('returned', models.BooleanField(blank=True, default=False, null=True)),
                ('notes', models.TextField(blank=True, max_length=448, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('asset_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.asset_type')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundle_reservation_requests_created', to='asset_app.locations')),
            ],
            options={
                'ordering': ['-return_date'],
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.model'),
        ),
        migrations.AddField(
            model_name='asset',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_app.room'),
        ),
    ]
