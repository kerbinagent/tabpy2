# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20150309_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='novice',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='novice',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
