# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20150311_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_stat',
            name='panel1',
            field=models.ForeignKey(related_name='panel1', blank=True, to='tournament.Judge', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room_stat',
            name='panel2',
            field=models.ForeignKey(related_name='panel2', blank=True, to='tournament.Judge', null=True),
            preserve_default=True,
        ),
    ]
