# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ballot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ballot_id', models.IntegerField(default=0, unique=True)),
                ('round_number', models.IntegerField(default=-1)),
                ('p1s', models.IntegerField(default=0)),
                ('p2s', models.IntegerField(default=0)),
                ('p3s', models.IntegerField(default=0)),
                ('o1s', models.IntegerField(default=0)),
                ('o2s', models.IntegerField(default=0)),
                ('o3s', models.IntegerField(default=0)),
                ('prs', models.FloatField(default=0)),
                ('ors', models.FloatField(default=0)),
                ('split', models.BooleanField(default=False)),
                ('judge', models.ForeignKey(related_name='judge', to='tournament.Judge')),
                ('o_1', models.ForeignKey(related_name='o_1', to='tournament.Speaker')),
                ('o_2', models.ForeignKey(related_name='o_2', to='tournament.Speaker')),
                ('o_3', models.ForeignKey(related_name='o_3', to='tournament.Speaker')),
                ('o_team', models.ForeignKey(related_name='o_team', to='tournament.Team')),
                ('p_1', models.ForeignKey(related_name='p_1', to='tournament.Speaker')),
                ('p_2', models.ForeignKey(related_name='p_2', to='tournament.Speaker')),
                ('p_3', models.ForeignKey(related_name='p_3', to='tournament.Speaker')),
                ('p_team', models.ForeignKey(related_name='p_team', to='tournament.Team')),
                ('room', models.ForeignKey(related_name='room', to='tournament.Room')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_admin', models.BooleanField(default=False)),
                ('judge', models.OneToOneField(null=True, blank=True, to='tournament.Judge')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
