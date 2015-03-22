# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_tournament_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge_feedback',
            name='feedback_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament_feedback',
            name='feedback_text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
