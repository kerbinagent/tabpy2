# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_auto_20150311_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='po_str',
            field=models.CharField(default=b'', max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
