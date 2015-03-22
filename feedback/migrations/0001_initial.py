# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='judge_feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fair_score', models.IntegerField(choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('clarity_score', models.IntegerField(choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('friendly_score', models.IntegerField(choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('knowledge_score', models.IntegerField(choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('availability_score', models.IntegerField(choices=[(b'1', 1), (b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('feedback_text', models.TextField()),
                ('judge', models.ForeignKey(to='tournament.Judge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
