# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, max_length=2048, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArtistGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('url', models.URLField(blank=True, max_length=2048, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('artists', models.ManyToManyField(to='artwork.Artist')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('doc', models.FileField(upload_to='document')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'equipment',
            },
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('provider', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, max_length=1024, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('opened', models.DateTimeField(blank=True, null=True)),
                ('closed', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('artists', models.ManyToManyField(blank=True, to='artwork.Artist')),
                ('documents', models.ManyToManyField(blank=True, to='artwork.Document')),
                ('groups', models.ManyToManyField(blank=True, to='artwork.ArtistGroup')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'artwork',
                'verbose_name_plural': 'works of art',
            },
        ),
        migrations.CreateModel(
            name='InstallationSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('location', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ManyToManyField(blank=True, to='artwork.Equipment')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photo')),
                ('title', models.TextField(blank=True, null=True)),
                ('caption', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='installationsite',
            name='photos',
            field=models.ManyToManyField(blank=True, to='artwork.Photo'),
        ),
        migrations.AddField(
            model_name='installation',
            name='photos',
            field=models.ManyToManyField(blank=True, to='artwork.Photo'),
        ),
        migrations.AddField(
            model_name='installation',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='artwork.InstallationSite'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='equipment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artwork.EquipmentType'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='photos',
            field=models.ManyToManyField(blank=True, to='artwork.Photo'),
        ),
    ]