# Generated by Django 4.2.5 on 2023-12-17 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0017_qrd_short_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrd',
            name='qrd_date',
            field=models.DateField(default=datetime.date(2023, 12, 17)),
        ),
    ]
