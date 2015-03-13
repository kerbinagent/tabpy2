# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('name', models.CharField(max_length=64, unique=True, serialize=False, primary_key=True)),
                ('code', models.CharField(default=b'CODE', unique=True, max_length=8)),
                ('weight', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('distance_to_hall', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room_Stat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField(default=1)),
                ('chair', models.ForeignKey(to='tournament.Judge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('speaker_id', models.IntegerField(default=0, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('total_sp', models.IntegerField(default=0)),
                ('school', models.ForeignKey(to='tournament.School')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpeakerPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField(default=1)),
                ('point', models.IntegerField(default=0)),
                ('speaker_id', models.ForeignKey(to='tournament.Speaker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'open', unique=True, max_length=64)),
                ('total_wl', models.IntegerField(default=0)),
                ('total_po', models.IntegerField(default=0)),
                ('total_sp', models.IntegerField(default=0)),
                ('total_mg', models.IntegerField(default=0)),
                ('slug', models.SlugField(default=b'open', unique=True, max_length=128)),
                ('school', models.ForeignKey(to='tournament.School')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='speaker',
            name='team',
            field=models.ForeignKey(to='tournament.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='oppo_team',
            field=models.ForeignKey(related_name='oppo_team', to='tournament.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='panel1',
            field=models.ForeignKey(related_name='panel1', to='tournament.Judge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='panel2',
            field=models.ForeignKey(related_name='panel2', to='tournament.Judge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='prop_team',
            field=models.ForeignKey(related_name='prop_team', to='tournament.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='room_id',
            field=models.ForeignKey(to='tournament.Room'),
            preserve_default=True,
        ),
    ]
