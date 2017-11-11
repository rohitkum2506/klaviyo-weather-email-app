# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signupform', '0003_auto_20150722_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weathersubscription',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
