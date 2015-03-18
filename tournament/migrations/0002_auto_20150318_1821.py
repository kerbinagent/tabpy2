# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='contact_email',
            field=models.EmailField(default=b'example@example.com', max_length=75),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_number',
            field=models.IntegerField(default=10000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='contact_person',
            field=models.CharField(default=b'None', max_length=32),
            preserve_default=True,
        ),
    ]
