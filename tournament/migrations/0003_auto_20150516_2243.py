# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_room_stat_matchup_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='code',
        ),
        migrations.RemoveField(
            model_name='judge',
            name='round_filled',
        ),
    ]
