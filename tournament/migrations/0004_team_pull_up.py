# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_auto_20150309_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='pull_up',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
