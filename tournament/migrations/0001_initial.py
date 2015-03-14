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
                ('round_filled', models.IntegerField(default=0)),
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
                ('novice', models.BooleanField(default=False)),
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
                ('name', models.CharField(unique=True, max_length=64)),
                ('total_wl', models.IntegerField(default=0)),
                ('total_po', models.IntegerField(default=0)),
                ('po_str', models.CharField(default=b'', max_length=32, blank=True)),
                ('total_sp', models.FloatField(default=0)),
                ('total_mg', models.FloatField(default=0)),
                ('novice', models.BooleanField(default=False)),
                ('pull_up', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('school', models.ForeignKey(to='tournament.School')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament_Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name_of_Tournament', models.CharField(default=b'new tournament', max_length=64)),
                ('Max_Margin', models.IntegerField(default=300)),
                ('Total_Rounds', models.IntegerField(default=8)),
                ('Novice_Breaks', models.IntegerField(default=4)),
                ('Breaks', models.IntegerField(default=16)),
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
            field=models.ForeignKey(related_name='panel1', blank=True, to='tournament.Judge', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room_stat',
            name='panel2',
            field=models.ForeignKey(related_name='panel2', blank=True, to='tournament.Judge', null=True),
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